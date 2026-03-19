/// AI Cards — Pack Payment Module
/// Users pay SUI to a treasury, server mints cards.
/// Treasury is a shared object that accumulates SUI from pack purchases.
#[allow(lint(self_transfer))]
module aicards::payment {
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::balance::{Self, Balance};
    use sui::event;
    use std::string::String;

    // ═══════════════════════════════════════
    // TREASURY
    // ═══════════════════════════════════════
    /// Shared object that holds SUI from pack purchases.
    /// Only the admin (via AdminCap from card module) can withdraw.
    public struct Treasury has key {
        id: UID,
        balance: Balance<SUI>,
        /// Price per pack in MIST (1 SUI = 1_000_000_000 MIST)
        pack_price: u64,
        /// Total packs purchased
        total_packs: u64,
        /// Admin address (for withdrawal auth)
        admin: address,
    }

    // ═══════════════════════════════════════
    // EVENTS
    // ═══════════════════════════════════════
    public struct PackPurchased has copy, drop {
        buyer: address,
        pack_type: String,
        amount_paid: u64,
        treasury_balance: u64,
    }

    public struct TreasuryWithdrawal has copy, drop {
        admin: address,
        amount: u64,
        remaining: u64,
    }

    // ═══════════════════════════════════════
    // INIT — create the treasury as a shared object
    // ═══════════════════════════════════════
    fun init(ctx: &mut TxContext) {
        let treasury = Treasury {
            id: object::new(ctx),
            balance: balance::zero<SUI>(),
            // Default: 0.5 SUI per pack (~$0.50 at current prices)
            pack_price: 500_000_000,
            total_packs: 0,
            admin: ctx.sender(),
        };
        transfer::share_object(treasury);
    }

    // ═══════════════════════════════════════
    // BUY PACK — user pays SUI, gets a receipt
    // ═══════════════════════════════════════
    /// User sends SUI to buy a pack. The server watches for PackPurchased
    /// events and mints cards to the buyer's address.
    public fun buy_pack(
        treasury: &mut Treasury,
        payment: Coin<SUI>,
        pack_type: String,
        ctx: &mut TxContext,
    ) {
        let amount = coin::value(&payment);
        assert!(amount >= treasury.pack_price, 0); // E_INSUFFICIENT_PAYMENT

        // If overpaid, return change
        if (amount > treasury.pack_price) {
            let mut payment = payment;
            let change = coin::split(&mut payment, amount - treasury.pack_price, ctx);
            transfer::public_transfer(change, ctx.sender());
            coin::put(&mut treasury.balance, payment);
        } else {
            coin::put(&mut treasury.balance, payment);
        };

        treasury.total_packs = treasury.total_packs + 1;

        event::emit(PackPurchased {
            buyer: ctx.sender(),
            pack_type,
            amount_paid: treasury.pack_price,
            treasury_balance: balance::value(&treasury.balance),
        });
    }

    // ═══════════════════════════════════════
    // ADMIN FUNCTIONS
    // ═══════════════════════════════════════
    /// Admin withdraws accumulated SUI from the treasury.
    public fun withdraw(
        treasury: &mut Treasury,
        amount: u64,
        ctx: &mut TxContext,
    ) {
        assert!(ctx.sender() == treasury.admin, 1); // E_NOT_ADMIN
        assert!(amount <= balance::value(&treasury.balance), 2); // E_INSUFFICIENT_BALANCE

        let withdrawn = coin::take(&mut treasury.balance, amount, ctx);
        transfer::public_transfer(withdrawn, treasury.admin);

        event::emit(TreasuryWithdrawal {
            admin: treasury.admin,
            amount,
            remaining: balance::value(&treasury.balance),
        });
    }

    /// Admin updates the pack price.
    public fun set_price(
        treasury: &mut Treasury,
        new_price: u64,
        ctx: &mut TxContext,
    ) {
        assert!(ctx.sender() == treasury.admin, 1); // E_NOT_ADMIN
        treasury.pack_price = new_price;
    }

    // ═══════════════════════════════════════
    // READ
    // ═══════════════════════════════════════
    public fun pack_price(treasury: &Treasury): u64 { treasury.pack_price }
    public fun total_packs(treasury: &Treasury): u64 { treasury.total_packs }
    public fun treasury_balance(treasury: &Treasury): u64 { balance::value(&treasury.balance) }

    // ═══════════════════════════════════════
    // TEST HELPER
    // ═══════════════════════════════════════
    #[test_only]
    public fun init_for_testing(ctx: &mut TxContext) {
        init(ctx);
    }
}
