partner = "Uhaul-Interstate"
scenario = "Driver of Uhaul TRK-205 had to take an unapproved 30-mile detour on state roads due to heavy traffic on the designated interstate to make up time. They did not inform Maverick dispatch or Uhaul dispatch about the route change but believe they will still arrive close to the original ETA."
analysis = analyze_scenario_compliance(partner, scenario)
print(f"\nGemini's Compliance Analysis for {partner} Scenario:")
print(to_markdown(analysis))