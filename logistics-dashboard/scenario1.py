partner = "Amazon-Prime"
scenario = "Shipment MAV-AMZ-789 to Boston is now projected to be 5 hours late due to an unexpected highway closure from an accident. Original ETA was 14:00 EST. Dispatch has not yet been able to reach the Amazon Logistics contact."
analysis = analyze_scenario_compliance(partner, scenario)
print(f"\nGemini's Compliance Analysis for {partner} Scenario:")
print(to_markdown(analysis))