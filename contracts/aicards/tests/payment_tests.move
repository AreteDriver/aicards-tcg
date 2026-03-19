#[test_only]
module aicards::payment_tests {
    use aicards::payment::{Self, Treasury};
    use sui::test_scenario;
    use sui::coin;
    use sui::sui::SUI;

    const ADMIN: address = @0xAD;
    const BUYER: address = @0xBEEF;

    #[test]
    fun test_buy_pack() {
        let mut scenario = test_scenario::begin(ADMIN);
        {
            payment::init_for_testing(scenario.ctx());
        };
        // Treasury is now shared
        scenario.next_tx(BUYER);
        {
            let mut treasury = test_scenario::take_shared<Treasury>(&scenario);
            let price = payment::pack_price(&treasury);
            assert!(price == 500_000_000); // 0.5 SUI

            // Create payment coin
            let payment = coin::mint_for_testing<SUI>(price, scenario.ctx());
            payment::buy_pack(&mut treasury, payment, b"standard".to_string(), scenario.ctx());

            assert!(payment::total_packs(&treasury) == 1);
            assert!(payment::treasury_balance(&treasury) == price);

            test_scenario::return_shared(treasury);
        };
        scenario.end();
    }

    #[test]
    fun test_buy_pack_with_change() {
        let mut scenario = test_scenario::begin(ADMIN);
        {
            payment::init_for_testing(scenario.ctx());
        };
        scenario.next_tx(BUYER);
        {
            let mut treasury = test_scenario::take_shared<Treasury>(&scenario);
            let price = payment::pack_price(&treasury);

            // Overpay by 100_000_000
            let payment = coin::mint_for_testing<SUI>(price + 100_000_000, scenario.ctx());
            payment::buy_pack(&mut treasury, payment, b"jobless".to_string(), scenario.ctx());

            // Treasury should only have the pack price
            assert!(payment::treasury_balance(&treasury) == price);
            test_scenario::return_shared(treasury);
        };
        // Buyer should have received change
        scenario.next_tx(BUYER);
        {
            let change = test_scenario::take_from_sender<coin::Coin<SUI>>(&scenario);
            assert!(coin::value(&change) == 100_000_000);
            test_scenario::return_to_sender(&scenario, change);
        };
        scenario.end();
    }

    #[test]
    fun test_admin_withdraw() {
        let mut scenario = test_scenario::begin(ADMIN);
        {
            payment::init_for_testing(scenario.ctx());
        };
        // Buyer purchases a pack
        scenario.next_tx(BUYER);
        {
            let mut treasury = test_scenario::take_shared<Treasury>(&scenario);
            let price = payment::pack_price(&treasury);
            let payment = coin::mint_for_testing<SUI>(price, scenario.ctx());
            payment::buy_pack(&mut treasury, payment, b"standard".to_string(), scenario.ctx());
            test_scenario::return_shared(treasury);
        };
        // Admin withdraws
        scenario.next_tx(ADMIN);
        {
            let mut treasury = test_scenario::take_shared<Treasury>(&scenario);
            payment::withdraw(&mut treasury, 200_000_000, scenario.ctx());
            assert!(payment::treasury_balance(&treasury) == 300_000_000);
            test_scenario::return_shared(treasury);
        };
        scenario.end();
    }

    #[test]
    fun test_set_price() {
        let mut scenario = test_scenario::begin(ADMIN);
        {
            payment::init_for_testing(scenario.ctx());
        };
        scenario.next_tx(ADMIN);
        {
            let mut treasury = test_scenario::take_shared<Treasury>(&scenario);
            payment::set_price(&mut treasury, 1_000_000_000, scenario.ctx()); // 1 SUI
            assert!(payment::pack_price(&treasury) == 1_000_000_000);
            test_scenario::return_shared(treasury);
        };
        scenario.end();
    }

    #[test]
    #[expected_failure]
    fun test_non_admin_cannot_withdraw() {
        let mut scenario = test_scenario::begin(ADMIN);
        {
            payment::init_for_testing(scenario.ctx());
        };
        // Non-admin tries to withdraw
        scenario.next_tx(BUYER);
        {
            let mut treasury = test_scenario::take_shared<Treasury>(&scenario);
            payment::withdraw(&mut treasury, 0, scenario.ctx()); // should fail
            test_scenario::return_shared(treasury);
        };
        scenario.end();
    }
}
