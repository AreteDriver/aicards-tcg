/// AI Cards — 2030 Survival Edition
/// On-chain collectible card game about AI displacement.
/// Cards are owned Sui objects that can be freely transferred/traded.
module aicards::card {
    use std::string::String;
    use sui::display;
    use sui::package;
    use sui::event;

    // ═══════════════════════════════════════
    // OTW for Display + Publisher
    // ═══════════════════════════════════════
    public struct CARD has drop {}

    // ═══════════════════════════════════════
    // CARD NFT
    // ═══════════════════════════════════════
    /// Each card is a unique owned object. `store` enables Kiosk trading.
    public struct Card has key, store {
        id: UID,
        /// Internal card identifier (e.g., "plumber", "ds-whistleblower")
        card_id: String,
        /// Display name (e.g., "THE PLUMBER")
        name: String,
        /// MYTHIC | LEGENDARY | RARE | UNCOMMON | COMMON | JUNK
        rarity: String,
        /// Category (e.g., "Human Trade", "AI Product", "Irreplaceable")
        category: String,
        /// Set this card belongs to
        set: String,
        /// Karpathy AI exposure score (0-10, or "∞")
        kscore: String,
        /// Attack stat
        atk: String,
        /// Defense stat
        def: String,
        /// Named ability + flavor text
        flavor: String,
        /// Emoji symbol
        symbol: String,
        /// Card number within set (for display ordering)
        number: u64,
        /// Image URL (can point to aicards.fun/cards/{card_id}.png or IPFS)
        image_url: String,
    }

    // ═══════════════════════════════════════
    // ADMIN CAP
    // ═══════════════════════════════════════
    /// Only the admin can mint cards and create packs.
    public struct AdminCap has key, store {
        id: UID,
    }

    // ═══════════════════════════════════════
    // EVENTS
    // ═══════════════════════════════════════
    public struct CardMinted has copy, drop {
        card_object_id: ID,
        card_id: String,
        rarity: String,
        set: String,
        recipient: address,
    }

    public struct PackOpened has copy, drop {
        pack_type: String,
        opener: address,
        card_ids: vector<ID>,
    }

    // ═══════════════════════════════════════
    // INIT — publish Display + AdminCap
    // ═══════════════════════════════════════
    fun init(otw: CARD, ctx: &mut TxContext) {
        let publisher = package::claim(otw, ctx);

        // Sui Display standard — wallets/explorers render cards using these fields
        let mut disp = display::new<Card>(&publisher, ctx);
        display::add(&mut disp, b"name".to_string(), b"{name}".to_string());
        display::add(&mut disp, b"description".to_string(), b"{rarity} · {category} · K-Score: {kscore} · ATK: {atk} / DEF: {def}".to_string());
        display::add(&mut disp, b"image_url".to_string(), b"{image_url}".to_string());
        display::add(&mut disp, b"project_url".to_string(), b"https://aicards.fun".to_string());
        display::add(&mut disp, b"creator".to_string(), b"AreteDriver".to_string());
        display::update_version(&mut disp);

        transfer::public_transfer(publisher, ctx.sender());
        transfer::public_transfer(disp, ctx.sender());

        // AdminCap to the deployer
        transfer::transfer(AdminCap { id: object::new(ctx) }, ctx.sender());
    }

    // ═══════════════════════════════════════
    // MINT — admin mints a single card to a recipient
    // ═══════════════════════════════════════
    public fun mint(
        _admin: &AdminCap,
        card_id: String,
        name: String,
        rarity: String,
        category: String,
        set: String,
        kscore: String,
        atk: String,
        def: String,
        flavor: String,
        symbol: String,
        number: u64,
        image_url: String,
        recipient: address,
        ctx: &mut TxContext,
    ) {
        let card = Card {
            id: object::new(ctx),
            card_id,
            name,
            rarity,
            category,
            set,
            kscore,
            atk,
            def,
            flavor,
            symbol,
            number,
            image_url,
        };

        event::emit(CardMinted {
            card_object_id: object::id(&card),
            card_id: card.card_id,
            rarity: card.rarity,
            set: card.set,
            recipient,
        });

        transfer::public_transfer(card, recipient);
    }

    // ═══════════════════════════════════════
    // MINT PACK — admin mints 5 cards at once
    // ═══════════════════════════════════════
    /// Batch mint 5 cards to a recipient (server determines rarity off-chain,
    /// sends the resolved card data). This keeps gas costs predictable.
    public fun mint_pack(
        _admin: &AdminCap,
        pack_type: String,
        // Card 1
        c1_card_id: String, c1_name: String, c1_rarity: String, c1_category: String,
        c1_set: String, c1_kscore: String, c1_atk: String, c1_def: String,
        c1_flavor: String, c1_symbol: String, c1_number: u64, c1_image_url: String,
        // Card 2
        c2_card_id: String, c2_name: String, c2_rarity: String, c2_category: String,
        c2_set: String, c2_kscore: String, c2_atk: String, c2_def: String,
        c2_flavor: String, c2_symbol: String, c2_number: u64, c2_image_url: String,
        // Card 3
        c3_card_id: String, c3_name: String, c3_rarity: String, c3_category: String,
        c3_set: String, c3_kscore: String, c3_atk: String, c3_def: String,
        c3_flavor: String, c3_symbol: String, c3_number: u64, c3_image_url: String,
        // Card 4
        c4_card_id: String, c4_name: String, c4_rarity: String, c4_category: String,
        c4_set: String, c4_kscore: String, c4_atk: String, c4_def: String,
        c4_flavor: String, c4_symbol: String, c4_number: u64, c4_image_url: String,
        // Card 5
        c5_card_id: String, c5_name: String, c5_rarity: String, c5_category: String,
        c5_set: String, c5_kscore: String, c5_atk: String, c5_def: String,
        c5_flavor: String, c5_symbol: String, c5_number: u64, c5_image_url: String,
        recipient: address,
        ctx: &mut TxContext,
    ) {
        let mut card_ids = vector::empty<ID>();

        // Mint card 1
        let card1 = Card {
            id: object::new(ctx), card_id: c1_card_id, name: c1_name, rarity: c1_rarity,
            category: c1_category, set: c1_set, kscore: c1_kscore, atk: c1_atk, def: c1_def,
            flavor: c1_flavor, symbol: c1_symbol, number: c1_number, image_url: c1_image_url,
        };
        vector::push_back(&mut card_ids, object::id(&card1));
        transfer::public_transfer(card1, recipient);

        // Mint card 2
        let card2 = Card {
            id: object::new(ctx), card_id: c2_card_id, name: c2_name, rarity: c2_rarity,
            category: c2_category, set: c2_set, kscore: c2_kscore, atk: c2_atk, def: c2_def,
            flavor: c2_flavor, symbol: c2_symbol, number: c2_number, image_url: c2_image_url,
        };
        vector::push_back(&mut card_ids, object::id(&card2));
        transfer::public_transfer(card2, recipient);

        // Mint card 3
        let card3 = Card {
            id: object::new(ctx), card_id: c3_card_id, name: c3_name, rarity: c3_rarity,
            category: c3_category, set: c3_set, kscore: c3_kscore, atk: c3_atk, def: c3_def,
            flavor: c3_flavor, symbol: c3_symbol, number: c3_number, image_url: c3_image_url,
        };
        vector::push_back(&mut card_ids, object::id(&card3));
        transfer::public_transfer(card3, recipient);

        // Mint card 4
        let card4 = Card {
            id: object::new(ctx), card_id: c4_card_id, name: c4_name, rarity: c4_rarity,
            category: c4_category, set: c4_set, kscore: c4_kscore, atk: c4_atk, def: c4_def,
            flavor: c4_flavor, symbol: c4_symbol, number: c4_number, image_url: c4_image_url,
        };
        vector::push_back(&mut card_ids, object::id(&card4));
        transfer::public_transfer(card4, recipient);

        // Mint card 5
        let card5 = Card {
            id: object::new(ctx), card_id: c5_card_id, name: c5_name, rarity: c5_rarity,
            category: c5_category, set: c5_set, kscore: c5_kscore, atk: c5_atk, def: c5_def,
            flavor: c5_flavor, symbol: c5_symbol, number: c5_number, image_url: c5_image_url,
        };
        vector::push_back(&mut card_ids, object::id(&card5));
        transfer::public_transfer(card5, recipient);

        event::emit(PackOpened {
            pack_type,
            opener: recipient,
            card_ids,
        });
    }

    // ═══════════════════════════════════════
    // READ — public accessors for off-chain indexing
    // ═══════════════════════════════════════
    public fun card_id(card: &Card): &String { &card.card_id }
    public fun name(card: &Card): &String { &card.name }
    public fun rarity(card: &Card): &String { &card.rarity }
    public fun category(card: &Card): &String { &card.category }
    public fun set(card: &Card): &String { &card.set }
    public fun kscore(card: &Card): &String { &card.kscore }
    public fun atk(card: &Card): &String { &card.atk }
    public fun def(card: &Card): &String { &card.def }
    public fun flavor(card: &Card): &String { &card.flavor }
    public fun symbol(card: &Card): &String { &card.symbol }
    public fun number(card: &Card): u64 { card.number }

    // ═══════════════════════════════════════
    // TEST HELPER
    // ═══════════════════════════════════════
    #[test_only]
    public fun init_for_testing(ctx: &mut TxContext) {
        init(CARD {}, ctx);
    }

    // ═══════════════════════════════════════
    // BURN — owner can destroy their card
    // ═══════════════════════════════════════
    public fun burn(card: Card) {
        let Card { id, card_id: _, name: _, rarity: _, category: _, set: _,
            kscore: _, atk: _, def: _, flavor: _, symbol: _, number: _, image_url: _ } = card;
        object::delete(id);
    }
}
