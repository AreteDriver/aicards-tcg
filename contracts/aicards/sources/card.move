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
    // MINT PACK — admin mints a variable-size pack at once
    // ═══════════════════════════════════════
    const EPackFieldLenMismatch: u64 = 1;

    /// Batch mint a pack of cards to a recipient. Server resolves rarities
    /// off-chain and sends parallel vectors (one entry per card). Vector-based
    /// so pack size can change without a contract redeploy — current game
    /// default is 10 cards per pack.
    public fun mint_pack(
        _admin: &AdminCap,
        pack_type: String,
        card_ids_in: vector<String>,
        names: vector<String>,
        rarities: vector<String>,
        categories: vector<String>,
        sets: vector<String>,
        kscores: vector<String>,
        atks: vector<String>,
        defs: vector<String>,
        flavors: vector<String>,
        symbols: vector<String>,
        numbers: vector<u64>,
        image_urls: vector<String>,
        recipient: address,
        ctx: &mut TxContext,
    ) {
        let n = vector::length(&card_ids_in);
        assert!(vector::length(&names) == n, EPackFieldLenMismatch);
        assert!(vector::length(&rarities) == n, EPackFieldLenMismatch);
        assert!(vector::length(&categories) == n, EPackFieldLenMismatch);
        assert!(vector::length(&sets) == n, EPackFieldLenMismatch);
        assert!(vector::length(&kscores) == n, EPackFieldLenMismatch);
        assert!(vector::length(&atks) == n, EPackFieldLenMismatch);
        assert!(vector::length(&defs) == n, EPackFieldLenMismatch);
        assert!(vector::length(&flavors) == n, EPackFieldLenMismatch);
        assert!(vector::length(&symbols) == n, EPackFieldLenMismatch);
        assert!(vector::length(&numbers) == n, EPackFieldLenMismatch);
        assert!(vector::length(&image_urls) == n, EPackFieldLenMismatch);

        let mut card_ids_out = vector::empty<ID>();

        let mut card_ids_in = card_ids_in;
        let mut names = names;
        let mut rarities = rarities;
        let mut categories = categories;
        let mut sets = sets;
        let mut kscores = kscores;
        let mut atks = atks;
        let mut defs = defs;
        let mut flavors = flavors;
        let mut symbols = symbols;
        let mut numbers = numbers;
        let mut image_urls = image_urls;

        let mut i = 0;
        while (i < n) {
            let card = Card {
                id: object::new(ctx),
                card_id: vector::pop_back(&mut card_ids_in),
                name: vector::pop_back(&mut names),
                rarity: vector::pop_back(&mut rarities),
                category: vector::pop_back(&mut categories),
                set: vector::pop_back(&mut sets),
                kscore: vector::pop_back(&mut kscores),
                atk: vector::pop_back(&mut atks),
                def: vector::pop_back(&mut defs),
                flavor: vector::pop_back(&mut flavors),
                symbol: vector::pop_back(&mut symbols),
                number: vector::pop_back(&mut numbers),
                image_url: vector::pop_back(&mut image_urls),
            };
            vector::push_back(&mut card_ids_out, object::id(&card));
            transfer::public_transfer(card, recipient);
            i = i + 1;
        };

        vector::destroy_empty(card_ids_in);
        vector::destroy_empty(names);
        vector::destroy_empty(rarities);
        vector::destroy_empty(categories);
        vector::destroy_empty(sets);
        vector::destroy_empty(kscores);
        vector::destroy_empty(atks);
        vector::destroy_empty(defs);
        vector::destroy_empty(flavors);
        vector::destroy_empty(symbols);
        vector::destroy_empty(numbers);
        vector::destroy_empty(image_urls);

        event::emit(PackOpened {
            pack_type,
            opener: recipient,
            card_ids: card_ids_out,
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
