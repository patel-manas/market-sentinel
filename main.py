from src.collectors.us_market import USMarketCollector


def main():
    print("🚀 Running US Market Data Collector...\n")

    collector = USMarketCollector()
    snapshots = collector.fetch()

    print("--- US MARKET SUMMARY ---")
    for s in snapshots:
        direction = "+" if s.change_pct >= 0 else ""
        print(f"{s.name:<12} ({s.symbol:<6}): {s.price:>8.2f} | {direction}{s.change_pct}%")

    print("\n✅ US Market Data Collection Successful!")


if __name__ == "__main__":
    main()