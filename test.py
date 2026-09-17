import polars as pl

hands = pl.scan_parquet("data/hands/*.parquet")
players = pl.scan_parquet("data/player_hands/*.parquet")
actions = pl.scan_parquet("data/actions/*.parquet")

# -------------------------
# Core counts
# -------------------------

hand_count = hands.select(
    pl.len().alias("total_hands")
)

unique_hand_count = hands.select(
    pl.col("hand_id").n_unique().alias("unique_hand_ids")
)

player_row_count = players.select(
    pl.len().alias("player_hand_rows")
)

unique_players = players.select(
    pl.col("player_id").n_unique().alias("unique_players")
)

action_count = actions.select(
    pl.len().alias("total_actions")
)

# -------------------------
# Data quality checks
# -------------------------

duplicate_hands = (
    hands
    .group_by("hand_id")
    .agg(pl.len().alias("count"))
    .filter(pl.col("count") > 1)
    .select(pl.len().alias("duplicate_hand_ids"))
)

missing_hand_fields = hands.select([
    pl.col("hand_id").null_count().alias("missing_hand_id"),
    pl.col("datetime").null_count().alias("missing_datetime"),
    pl.col("venue").null_count().alias("missing_venue"),
    pl.col("table").null_count().alias("missing_table"),
])

missing_player_fields = players.select([
    pl.col("player_id").null_count().alias("missing_player_id"),
    pl.col("starting_stack").null_count().alias("missing_starting_stack"),
    pl.col("seat").null_count().alias("missing_seat"),
    pl.col("winnings").null_count().alias("missing_winnings"),
])

# -------------------------
# Relationship checks
# -------------------------

players_without_hand = (
    players
    .join(
        hands.select("hand_id"),
        on="hand_id",
        how="anti"
    )
    .select(pl.len().alias("player_rows_without_hand"))
)

actions_without_hand = (
    actions
    .join(
        hands.select("hand_id"),
        on="hand_id",
        how="anti"
    )
    .select(pl.len().alias("action_rows_without_hand"))
)

# Compare players_dealt against actual player rows
player_counts_per_hand = (
    players
    .group_by("hand_id")
    .agg(
        pl.len().alias("actual_player_rows")
    )
)

player_count_mismatches = (
    hands
    .select(["hand_id", "players_dealt"])
    .join(
        player_counts_per_hand,
        on="hand_id",
        how="left"
    )
    .filter(
        pl.col("players_dealt") !=
        pl.col("actual_player_rows")
    )
    .select(
        pl.len().alias("player_count_mismatches")
    )
)

# -------------------------
# Useful distributions
# -------------------------

players_per_hand = (
    hands
    .group_by("players_dealt")
    .agg(pl.len().alias("hands"))
    .sort("players_dealt")
)

venues = (
    hands
    .group_by("venue")
    .agg(pl.len().alias("hands"))
    .sort("hands", descending=True)
)

date_range = hands.select([
    pl.col("datetime").min().alias("earliest_hand"),
    pl.col("datetime").max().alias("latest_hand"),
])

# -------------------------
# Run everything
# -------------------------

print("\n=== CORE COUNTS ===")
print(pl.collect_all([
    hand_count,
    unique_hand_count,
    player_row_count,
    unique_players,
    action_count,
]))

print("\n=== DUPLICATE HAND CHECK ===")
print(duplicate_hands.collect())

print("\n=== MISSING HAND DATA ===")
print(missing_hand_fields.collect())

print("\n=== MISSING PLAYER DATA ===")
print(missing_player_fields.collect())

print("\n=== RELATIONSHIP CHECKS ===")
print(pl.collect_all([
    players_without_hand,
    actions_without_hand,
    player_count_mismatches,
]))

print("\n=== PLAYERS DEALT PER HAND ===")
print(players_per_hand.collect())

print("\n=== VENUES ===")
print(venues.collect())

print("\n=== DATE RANGE ===")
print(date_range.collect())