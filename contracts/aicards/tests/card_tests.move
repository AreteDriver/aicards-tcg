#[test_only]
module aicards::card_tests {
    use aicards::card::{Self, Card, AdminCap};
    use sui::test_scenario;

    const ADMIN: address = @0xAD;
    const USER: address = @0xBEEF;

    #[test]
    fun test_init_creates_admin_cap() {
        let mut scenario = test_scenario::begin(ADMIN);
        {
            card::init_for_testing(scenario.ctx());
        };
        scenario.next_tx(ADMIN);
        {
            // AdminCap should exist for the deployer
            assert!(test_scenario::has_most_recent_for_sender<AdminCap>(&scenario));
        };
        scenario.end();
    }

    #[test]
    fun test_mint_single_card() {
        let mut scenario = test_scenario::begin(ADMIN);
        {
            card::init_for_testing(scenario.ctx());
        };
        scenario.next_tx(ADMIN);
        {
            let admin_cap = test_scenario::take_from_sender<AdminCap>(&scenario);
            card::mint(
                &admin_cap,
                b"plumber".to_string(),
                b"THE PLUMBER".to_string(),
                b"LEGENDARY".to_string(),
                b"Human Trade".to_string(),
                b"2030 Survival".to_string(),
                b"2".to_string(),
                b"550K".to_string(),
                b"SHORTAGE".to_string(),
                b"While you were getting your MBA, a pipe burst.".to_string(),
                b"\xF0\x9F\x94\xA7".to_string(), // 🔧
                1,
                b"https://aicards.fun/cards/plumber.png".to_string(),
                USER,
                scenario.ctx(),
            );
            test_scenario::return_to_sender(&scenario, admin_cap);
        };
        scenario.next_tx(USER);
        {
            let card = test_scenario::take_from_sender<Card>(&scenario);
            assert!(card::name(&card) == &b"THE PLUMBER".to_string());
            assert!(card::rarity(&card) == &b"LEGENDARY".to_string());
            assert!(card::set(&card) == &b"2030 Survival".to_string());
            assert!(card::kscore(&card) == &b"2".to_string());
            assert!(card::number(&card) == 1);
            test_scenario::return_to_sender(&scenario, card);
        };
        scenario.end();
    }

    #[test]
    fun test_burn_card() {
        let mut scenario = test_scenario::begin(ADMIN);
        {
            card::init_for_testing(scenario.ctx());
        };
        scenario.next_tx(ADMIN);
        {
            let admin_cap = test_scenario::take_from_sender<AdminCap>(&scenario);
            card::mint(
                &admin_cap,
                b"prompt-engineer".to_string(),
                b"THE PROMPT ENGINEER".to_string(),
                b"JUNK".to_string(),
                b"Lore".to_string(),
                b"2030 Survival".to_string(),
                b"10".to_string(),
                b"0".to_string(),
                b"DEPRECATED".to_string(),
                b"Already obsolete.".to_string(),
                b"\xF0\x9F\x92\xAC".to_string(), // 💬
                42,
                b"https://aicards.fun/cards/prompt-engineer.png".to_string(),
                USER,
                scenario.ctx(),
            );
            test_scenario::return_to_sender(&scenario, admin_cap);
        };
        scenario.next_tx(USER);
        {
            let card = test_scenario::take_from_sender<Card>(&scenario);
            card::burn(card);
        };
        scenario.end();
    }

    #[test]
    fun test_card_transfer() {
        let other_user: address = @0xCAFE;
        let mut scenario = test_scenario::begin(ADMIN);
        {
            card::init_for_testing(scenario.ctx());
        };
        scenario.next_tx(ADMIN);
        {
            let admin_cap = test_scenario::take_from_sender<AdminCap>(&scenario);
            card::mint(
                &admin_cap,
                b"the-mother".to_string(),
                b"THE MOTHER".to_string(),
                b"MYTHIC".to_string(),
                b"Irreplaceable".to_string(),
                b"Jobless.ai".to_string(),
                b"0".to_string(),
                b"\xE2\x88\x9E".to_string(), // ∞
                b"\xE2\x88\x9E".to_string(), // ∞
                b"GPT-7 passed the Turing test. Her toddler didn't care.".to_string(),
                b"\xF0\x9F\x92\xAB".to_string(), // 💫
                1,
                b"https://aicards.fun/cards/the-mother.png".to_string(),
                USER,
                scenario.ctx(),
            );
            test_scenario::return_to_sender(&scenario, admin_cap);
        };
        // User transfers card to another user (trading!)
        scenario.next_tx(USER);
        {
            let card = test_scenario::take_from_sender<Card>(&scenario);
            transfer::public_transfer(card, other_user);
        };
        // Other user now owns it
        scenario.next_tx(other_user);
        {
            let card = test_scenario::take_from_sender<Card>(&scenario);
            assert!(card::name(&card) == &b"THE MOTHER".to_string());
            assert!(card::rarity(&card) == &b"MYTHIC".to_string());
            test_scenario::return_to_sender(&scenario, card);
        };
        scenario.end();
    }
}
