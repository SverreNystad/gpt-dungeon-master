# Feature Backlog — GPT Dungeon Master

> **Status:** Product proposals, not a statement of implemented functionality.  
> **Prepared:** 2026-11-08  
> **Basis:** The existing [README](../README.md) and 2026 competitive research on AI Dungeon, Friends & Fables, AI Realm, RPBuddy, Character.AI, Chub AI, SillyTavern and Latitude Voyage.  
> **Audience:** Product, engineering and design.  
> **Working scope:** AI game master for solo play first, with a path to persistent tabletop campaigns, shared worlds and multiplayer.

## Product thesis

**Build an AI game master that runs a consistent, playable world — not just a chatbot that writes fantasy prose.** The language model can narrate and interpret player intentions, but a separate game engine should own rules, state changes, inventory, time, location, quests and consequences. Players should be able to see and correct important facts.

Three jobs to be done:
1. **Play immediately:** Start a compelling solo adventure without a human GM or complicated setup.
2. **Keep playing:** Resume a campaign days later without the DM forgetting what happened or quietly changing the rules.
3. **Create and share:** Build worlds, NPCs and adventures that can be reused, exported, and eventually played with friends.

### Reading this backlog

- **P0 — Playable MVP:** Required to deliver a coherent, persistent solo campaign.
- **P1 — Competitive differentiation:** Makes the experience more like a living RPG than generic AI storytelling.
- **P2 — Expansion:** Creator network, advanced controls, additional platforms and ecosystem.
- **README planned** means the idea already appears in the repository's existing Planned Features section. **Research proposal** means this document introduces or substantially extends it.
- Neither label means the feature has been implemented. **Implementation status has not been audited against the codebase.** Reassess priorities after user testing and an architecture review.
- Each acceptance criterion is a **proposed test of completion**, not an existing automated test.

## P0 — Playable MVP

| ID | Feature | Acceptance criterion / minimum useful behavior | Origin |
| --- | --- | --- | --- |
| F-001 | Guided campaign onboarding | Player can pick a starter scenario, choose/create a character, and reach the first meaningful decision in a short guided flow; defaults require no rules expertise. | Research proposal; AI Dungeon, Friends & Fables |
| F-002 | Campaign persistence and save/resume | Create, list, resume and archive campaigns. Closing/reopening a session restores location, party, NPCs, quests, history and world state. | Research proposal; Friends & Fables, AI Realm |
| F-003 | Canonical structured game state | Store versioned entities for world, locations, characters, NPCs, factions, items, quests and time. Each accepted action produces an auditable state change, independent of the narration. | Research proposal; AI Realm, RPBuddy |
| F-004 | Validated action-to-narration pipeline | Interpret player intent into a proposed action; validate permissions/rules; roll or resolve; commit state atomically; then narrate the *actual* outcome. Invalid actions cannot silently mutate state. | Research proposal; Friends & Fables, Latitude Voyage |
| F-005 | Character sheets and progression | Show editable stats, abilities, HP, conditions, inventory and advancement. Picking up or using an item updates the sheet and is reflected in later responses. | Research proposal; AI Realm, Friends & Fables |
| F-006 | Dice rolls and configurable rule adjudication | Support transparent, logged dice rolls with modifiers and advantage/disadvantage where applicable. The resolver is deterministic given a recorded seed and ruleset; do not present improvised outcomes as official rules. | README planned (rule enforcement), expanded |
| F-007 | Grounded rules / knowledgebase retrieval | Load permitted reference material; retrieve relevant excerpts with source titles/sections; distinguish explicit rules from house rules and GM judgment. Prevent private/unlicensed rulebooks from being shared across users. | README planned (knowledgebase), expanded |
| F-008 | NPC profiles and relationship memory | Persist names, traits, goals, location, relationships, player-facing knowledge and NPC-private knowledge. When revisited after many turns, NPCs retain previously established details. | README planned (character interaction), expanded; AI Realm, RPBuddy |
| F-009 | Campaign journal, quest tracking and recaps | Track active/completed/failed quests and objective changes. Offer concise session summaries with links to relevant events; recap never invents canonical world changes. | Research proposal; Friends & Fables, AI Realm |
| F-010 | Interactive storytelling and player agency | Player can type freeform actions and talk to characters; AI narrates choices and consequences without arbitrarily taking control of the player character. Support tone, pacing and genre settings. | README planned (dynamic storytelling, character interaction, UI), expanded |
| F-011 | Long-term memory with inspectable facts | Separate recent conversation from durable facts. Show facts used by the GM, their source event and a correction/edit mechanism; relevant facts survive a 100-turn test scenario. | Research proposal; AI Realm, Chub, RPBuddy |
| F-012 | Automated campaign consistency tests | A fixed suite of multi-turn scenarios checks inventory conservation, HP, rules, location continuity, NPC knowledge, quest status and save/resume. Store reproducible traces and baseline pass rates. | Research proposal; foundational quality gate |

**MVP vertical slice:** A player starts a village quest, meets two NPCs, acquires an item, makes a rule-checked skill roll, travels, resolves an encounter, saves, returns later and receives a correct recap. The authoritative state must match the story at each step.

## P1 — Living world and richer play

| ID | Feature | Acceptance criterion / minimum useful behavior | Origin |
| --- | --- | --- | --- |
| F-013 | World builder and linked map | Creators can define regions, locations, points of interest and travel connections; player position is visible and narration respects map adjacency. Hex or node maps can be explored as implementations. | Research proposal; RPBuddy, Friends & Fables |
| F-014 | NPC schedules and off-screen goals | NPCs have locations, routines and goals that evolve when time advances; a merchant cannot simultaneously be at two distant locations. | Research proposal; RPBuddy |
| F-015 | NPC beliefs, gossip and hidden information | Each NPC knows only what they plausibly witnessed or learned. Rumors can propagate across social links with provenance and uncertainty; secrets are not leaked by default. | Research proposal; RPBuddy |
| F-016 | Factions, reputation and consequences | Record factions, alliances and reputation per player/party; meaningful choices alter attitudes, quest access or prices in subsequent scenes. | Research proposal; RPBuddy |
| F-017 | World clock, travel and event scheduling | Track elapsed time, weather/time-of-day where relevant, resting and travel duration. Scheduled events fire consistently when time advances. | Research proposal; AI Realm, RPBuddy |
| F-018 | Inventory economy, shops and crafting hooks | Define item quantities, currency, merchant stock and transactions; purchases and trades are validated and never create items or currency from nothing. | Research proposal; RPBuddy, Friends & Fables |
| F-019 | Tactical turn-based combat | Initiative, turn order, actions, resources, conditions, damage and outcomes are structured and replayable. Map-based positioning is optional initially; rules vary by active system. | Research proposal; Friends & Fables, RPBuddy |
| F-036 | Quick Time Events (QTEs) and timed decisions | At dramatic moments (e.g., dodging a trap, catching a falling ally, choosing whether to interrupt a ritual), display a clearly telegraphed countdown and 2–3 actions or freeform input. Each response, timeout or opt-out resolves through the authoritative game engine into a traceable outcome. Start the timer only after the event is visibly loaded; offer adjustable durations, pause/untimed mode, keyboard accessibility and a non-punitive fallback. Do not use reflex QTEs for every action. | New feature request; experiential design proposal |
| F-037 | Timed objectives and dynamic countdowns | Give players a configurable 30-second to 10-minute deadline to accomplish one or more objectives across multiple actions (e.g., evacuate a burning village). Support real-time or narrative-action-time modes, clear progress and remaining-time UI, partial successes, branching consequences, NPC assistance, and pause/untimed accessibility options. Countdown time must exclude AI generation latency; objectives and resolution must be authoritative, persistent and replay-safe. | User-requested feature; inspiration: Detroit: Become Human |
| F-020 | Consistent generative visual assets | Optionally generate portraits, locations, items or battle scenes; link assets to persistent entities and reuse them so appearances remain consistent. Support manual uploads and opt-out. | README planned (generative art), expanded |
| F-021 | Speech input and differentiated narration voices | Support speech-to-text and text-to-speech; users can mute/interrupt audio, and NPC voices remain associated with the correct character. | README planned (STT, TTS), expanded |
| F-022 | Synchronous and asynchronous multiplayer | Support invitations, party membership, turn ownership and shared state. Concurrent conflicting actions are serialized or resolved explicitly; absent players can catch up via recap. | Research proposal; Friends & Fables |
| F-023 | GM authoring controls and override mode | Creator/GM can edit locations, NPCs, lore and encounters; approved overrides update canonical state and appear in the audit log, rather than silently changing prompt text. | Research proposal; AI Realm, SillyTavern |
| F-024 | World/NPC/campaign import and export | Export a versioned machine-readable package with assets/licenses and import it into a new campaign; preserve stable entity IDs and validate schemas. Private user data is excluded by default. | Research proposal; Chub, SillyTavern |
| F-025 | Player safety, privacy and content preferences | Provide content boundaries and session controls, clear user-generated-content visibility, deletion/export options and safeguards for shared worlds. Avoid exposing private campaign data in logs or public assets. | Research proposal; platform foundation |

### QTE interaction specification (F-036)

**Player-facing example:** As a collapsing bridge breaks beneath the character, the AI DM describes the danger, and a short countdown presents: **Jump to the ledge**, **Grab the rope**, or **Shield your companion**. The player can also type a custom action when the input method supports it.

- **Triggering:** Only for meaningful, time-sensitive set pieces such as hazards, chases, tense negotiations or combat reactions; optional per campaign and tunable by the GM. Use deliberate author-controlled triggers or validated gameplay events, not a timer fabricated by narrative text.
- **Timing and fairness:** Make the deadline clear, configurable and generous by default. Start counting when the complete prompt and controls are rendered, not when text generation begins. Keep time synchronized with the game session and handle network interruption, reconnection and slow devices fairly.
- **Resolution:** The choice, timestamp, applicable ability/rules check, resulting state transition and narrative consequence are persisted once. Timeout chooses a documented fallback (e.g., miss the handhold, suffer a minor complication or defer to an untimed check), not arbitrary instant death.
- **Accessibility:** Offer untimed mode, adjustable countdowns, pause where appropriate, screen-reader announcements, full keyboard and pointer support, and reduced-motion presentation. Never make twitch reaction speed mandatory to continue the campaign.
- **Multiplayer:** Specify whose reaction is required and how the deadline applies to each player; avoid penalizing the entire party for lag or an absent player.

**QTE acceptance tests:** A completed action or timeout applies exactly one deterministic state transition; refreshing or reconnecting cannot duplicate outcomes; timers are not shortened by narration/model latency; changing the accessibility settings works before and during a campaign; untimed players can complete the same story branch.

### Timed objectives and dynamic countdowns (F-037)

**Design goal:** Create multi-action, high-stakes scenes with a deadline measured in minutes, inspired by the *time-pressure and branching-decision feel* of *Detroit: Become Human*. This is **not** the same as F-036: QTEs are short, reflex-oriented responses to a single prompt; **F-037 covers an entire scene with several decisions and objectives**. Both belong to a proposed **Time Pressure & Dynamic Events Engine**.

**Player-facing example — The Burning Village:** A fire is spreading through Blackthorn. The player has **3 minutes** to **alert the guards**, **rescue trapped children**, and **protect the granary**. Each goal has a visible state (pending / active / completed / failed). The player may choose among suggested actions, type a custom action, delegate to NPC allies, or accept a trade-off. A new threat (the roof begins collapsing) can appear as time passes. Saving the children but losing the granary is a valid partial success, with persistent effects on villagers, supplies, factions and future quests.

**Proposed behavior:**

1. **Start and presentation:** The game engine creates a structured timed scene with start/deadline, clock mode, objectives, dependencies, milestones, and outcomes. The UI shows a readable countdown, objective progress, stakes and any approaching deadlines. Begin ticking only after the scene and controls have been delivered to the client.
2. **Two clock modes:** **Real-time** advances while the player deliberates, excluding AI/model generation and processing delays; **narrative time** advances by predefined costs for actions (for example, searching a room takes 30 in-game seconds). The selected mode is visible before the event starts. Do not switch modes unexpectedly.
3. **Multiple actions:** Each player action can complete an objective, consume time, change risk, unlock another task or trigger an event. Allow freeform actions subject to validation by the same authoritative rules/state engine as normal play.
4. **Dynamic events:** At deterministic milestones (e.g., 50% time left, first rescue, a failed check), the engine may trigger predefined or validated emerging threats. Generated prose may *describe* events but does not control the authoritative clock or invent irreversible state transitions.
5. **Outcomes and consequences:** Resolve full completion, partial completion, timeout, abandonment and hard failures through an explicit outcome table or rules. Update quests, injuries, NPC status, reputation, world resources and journal exactly once. Do not force a total game-over on timeout by default.
6. **NPC and multiplayer interactions:** Allies may undertake delegated tasks with defined time and capability costs. Multiplayer sessions need server-authoritative deadlines, clear task ownership and lag/disconnect policies; no player should be penalized for another player's network failure.
7. **Fairness and accessibility:** Timer length and difficulty are configurable. Support adjustable duration, pause where possible, untimed/narrative-time modes, visible time warnings, keyboard/screen-reader access and reduced motion. Audio narration and TTS playback should not silently consume a player's response window; compensate or pause accordingly.
8. **Persistence and recovery:** Save the scene clock configuration, remaining logical time, objectives, decisions and event log; resume/reconnect without double applying outcomes or unexpectedly consuming time. For real-time multiplayer, define and communicate whether the event pauses when the session is suspended.
9. **Instrumentation:** Capture event starts, mode, selected actions, time spent on deliberation vs. model delay, objectives completed, timeout paths, skips, accessibility settings and subjective fairness; do not log unnecessary personal content.

**Acceptance criteria:**
- In the Burning Village scenario, the player can complete three objectives over multiple actions within an illustrated 3-minute deadline, or reach traceable partial-success and timeout endings.
- The countdown is **not reduced by model inference/network response delay**; real-time and narrative-time modes produce predictable results under controlled tests.
- Choices, NPC delegation, milestone events and expiry update canonical state **exactly once** even after retries, refreshes, disconnects or concurrent player actions.
- UI displays accurate remaining time, progress and consequences; an accessible untimed path preserves meaningful choices without reflex requirements.
- Automated tests verify deadline expiry, paused/resumed sessions, clock-mode switching restrictions, branching outcomes and a scene where the player saves only some targets.

**Implementation dependency:** Reuse F-003/F-004's canonical state-transition system and F-017's world clock; build F-036/F-037 on shared timed-event primitives rather than putting countdown business logic in an LLM prompt.

## P2 — Creator ecosystem and platform expansion

| ID | Feature | Acceptance criterion / minimum useful behavior | Origin |
| --- | --- | --- | --- |
| F-026 | Discoverable adventure/world library | Creators can publish, tag, search, rate and fork **opted-in** worlds or adventure templates, with attribution, moderation and removal controls. | Research proposal; AI Dungeon, Character.AI, Friends & Fables |
| F-027 | Portable character/NPC cards and lorebooks | Import/export documented character-card and triggered-lore formats; validate external content and let creators choose what enters active model context. | Research proposal; Chub, SillyTavern |
| F-028 | Ruleset adapters / house-rule modules | Add new licensed/open rules systems without rewriting the story engine. Ruleset version, modifications and precedence are visible in a campaign. | Research proposal; AI Realm, SillyTavern |
| F-029 | Model/provider selection and cost controls | Allow an operator or advanced user to compare approved model backends, latency and estimated inference cost. Protect API keys and apply per-campaign budget limits. | Research proposal; AI Dungeon, Chub, SillyTavern |
| F-030 | Natural-language world creation assistant | A creator can ask for a village, NPC cast, faction or quest and preview/approve generated structured entities before publication. | Research proposal; RPBuddy, Friends & Fables |
| F-031 | Bounded autonomous world simulation | Off-screen events update the world on scheduled ticks with budget caps, conflict handling and inspection. Events must not overwrite player actions or invent irreversible changes without a trace. | Research proposal; RPBuddy, Latitude Voyage |
| F-032 | Cross-device and mobile-friendly play | Campaign state and controls work across screen sizes; mobile view supports core actions and low-bandwidth mode. Consider PWA only after validating demand. | Research proposal; Friends & Fables, Everweave |
| F-033 | Multilingual worlds and narration | Narrate and accept actions in multiple languages while preserving language-neutral entity IDs and rules; tests cover names, dice notation and lore across languages. | Research proposal; differentiation hypothesis |
| F-034 | VTT and ecosystem integration | Export characters, dice history or encounter state to documented external formats/APIs; no hidden dependency on a specific vendor's proprietary content. | Research proposal; Friends & Fables, SillyTavern |
| F-035 | Shareable session recaps and creator clips | Create permission-checked summaries or visual recaps for a session; private information and unrevealed NPC secrets must be redacted. | Research proposal; acquisition hypothesis |

## Existing README feature coverage

The original README lists eight planned features. Preserve their intent; this backlog adds prioritization and concrete behavior rather than replacing them.

| README feature | Backlog links |
| --- | --- |
| Knowledgebase Integration | F-007 |
| Dynamic Storytelling | F-004, F-010 |
| Character Interaction | F-008, F-010, F-015 |
| Text-to-Speech | F-021 |
| Speech-to-Text | F-021 |
| Generative Art | F-020 |
| Rule Enforcement | F-004, F-006, F-028 |
| Interactive UI | F-001, F-010, F-032 |

## Suggested implementation sequence

| Milestone | Outcome | Feature IDs | Exit condition |
| --- | --- | --- | --- |
| M1 — Reliable solo core | One story with authoritative state and persistence | F-001–F-006, F-010 | Complete the MVP vertical slice; save/resume produces no divergent state |
| M2 — Memory and rules | Campaigns remain coherent over time | F-007–F-012 | Repeated 100-turn test scenarios meet the team's defined consistency threshold |
| M3 — Living campaign | World travel, NPC behavior and consequences | F-013–F-018, F-023 | Scheduled and social events are reproducible and inspectable |
| M4 — Rich campaign experience | Combat, QTEs, multi-minute timed objectives, visuals, voices and shared parties | F-019–F-022, F-025, F-036, F-037 | Integration tests cover combat, timed choice, multi-step objectives, countdown expiry/reconnect and concurrent actions; accessibility and privacy controls work |
| M5 — Platform and creator growth | Portable worlds and creator network | F-024, F-026–F-035 | At least one end-to-end import/export and a permission-checked publishing flow |

The sequence is a **proposal**; parallelize UX work and defer costly generation/simulation features if unit economics are not yet proven.

## Architectural requirements / non-functional features

1. **Authoritative state over prompt memory.** Use typed, validated domain objects and an event/audit log. LLM-generated text must never be the sole source of truth for HP, currency, location, quests or combat.
2. **Separate game logic from model providers.** Proposed pipeline: player input → intent extraction → rules/policy checks → deterministic state transition → event persistence → context retrieval → narration. Retry generation without duplicating state mutations.
3. **Bound context and inference cost.** Select relevant entity data instead of injecting the entire campaign every turn. Track tokens, latency, premium-model usage, images and voice spend per session.
4. **Consistency and debuggability.** Every mutating turn should have an event ID, relevant rule, state diff, dice result and model trace (with appropriate redaction). Make failed turns safely retryable.
5. **Schema evolution and backup.** Version campaign/world schemas, test migrations and support export/restore. Avoid losing long campaigns during upgrades.
6. **Content ownership and licensing.** Only ingest or publish materials that users/providers have rights to use. Review SRD licenses and required attribution before implementing any D&D-compatible rule text or creature data.
7. **Safety by design.** Keep private lore/secrets from public sharing, distinguish NPC-private from player-visible knowledge, protect minors and support configurable content boundaries.

## Prioritization and measurement

Do not decide priority by competitor feature counts alone. Test each proposal against player retention, experience quality and operating cost.

| Question / signal | Suggested measurement |
| --- | --- |
| Can a newcomer play successfully? | Onboarding completion, time to first meaningful action, first-session quest completion |
| Is the world consistent? | Errors per 100 turns: inventory, HP, chronology, NPC knowledge, quest contradictions, invalid rule resolutions |
| Do campaigns retain players? | D1/D7/D30 return rate, sessions per campaign, number of resumed campaigns, quest completion |
| Does memory actually help? | Controlled long-campaign evaluations with hidden facts revealed only to specific NPCs; correction success rate |
| Are simulation features valuable? | A/B test persistent NPC schedules vs simpler memory; qualitative interviews on perceived agency and world believability |
| Are timed decisions fun and fair? | QTE and multi-minute objective opt-in rate, objective completion/partial-success/timeout rates, accessibility mode usage, perceived fairness, model-latency-induced failures, and frequency of resumed scenes | 
| Can the economics scale? | Marginal cost per completed session, inference spend per retained player, P95 action latency, gross margin by feature |
| Does UGC create a flywheel? | Weekly active creators, playable assets published, imported/forked assets, creator-to-player conversion |

**Research hypotheses to validate with users:** persistent memory and state consistency may be more compelling than more elaborate prose; visible NPC agency may differentiate from chat products; creator portability may improve acquisition; mobile-first may broaden reach. None is a proven product-market-fit claim.

## Competitor-to-feature traceability

| Product | Useful benchmark | Features informed |
| --- | --- | --- |
| [RPBuddy](https://www.rpbuddy.ai/docs) | Persistent NPCs, hex-map worldbuilding, NPC routines, social simulation and a world that reacts to choices | F-008, F-013–F-018, F-030–F-031 |
| [Friends & Fables](https://fables.gg/) | Integrated AI GM, structured worldbuilding, quests, rules-inspired tactical combat, maps, creator worlds and multiplayer | F-002, F-005, F-009, F-013, F-019, F-022, F-026 |
| [AI Realm V2 Guide](https://airealm.com/home/v2Guide) | Editable NPC cards, GM guides, auto-updated campaign data, configurable context and character sheets | F-003, F-005, F-008, F-011, F-023 |
| [AI Dungeon](https://aidungeon.com/) | Low-friction freeform adventures, customizable scenarios, model options and community discovery | F-001, F-010, F-026, F-029 |
| [Chub documentation](https://docs.chub.ai/docs) | Portable character cards, lorebooks and external model/provider connections | F-011, F-024, F-027, F-029 |
| [SillyTavern](https://github.com/SillyTavern/SillyTavern) | Open tooling, advanced context control, model independence and extensibility | F-023, F-027–F-029, F-034 |
| [Character.AI creator/social product](https://blog.character.ai/character-ai-launches-worlds-first-ai-native-social-feed/) | Discovery, creator loops and sharing | F-026, F-035 |
| [Latitude Voyage announcement](https://latitude.io/news/voyage-launches-first-ai-native-rpg-platform) | Moving beyond freeform narration toward persistent world state and multiplayer | F-004, F-031 |

Sources reflect **publicly described capabilities** (competitive review completed August 2026, backlog prepared November 2026). Verify details again before relying on competitor-specific claims in future product decisions. **No competitor functionality has been copied as proprietary code or content.**

## Open product decisions

- Is the initial target a **solo narrative RPG**, a **5e-like tabletop simulation**, or a **human-GM copilot**? This backlog assumes solo AI GM as the first launch.
- Which rules are legally available to distribute and which should be optional user-supplied references?
- Do users want hard failure/death and strict dice adjudication, or story-first flexible play? Offer clear mode distinctions rather than silent switching.
- Will the initial release be local, browser-hosted, or a standalone app? This materially affects storage, authentication, cost and privacy.
- What are the acceptable per-session inference budget and latency thresholds?
- Will creators be allowed to monetize public worlds, and how will moderation, attribution and licensing work?

**Next engineering action:** turn F-001–F-012 into scoped issues, verify the current codebase before marking any complete, and build the M1 vertical-slice test as the primary delivery gate. Prototype F-036 as an optional timed hazard and F-037 as a multi-action Burning Village countdown after the authoritative state pipeline is stable.
