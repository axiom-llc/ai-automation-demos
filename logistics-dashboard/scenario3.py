partner = "Hertz-Local"
scenario = "The 'Service Engine Soon' light illuminated on Hertz van HZ-V07 at the start of the driver's shift this morning. The driver plans to report it at the end of their 8-hour shift today."
analysis = analyze_scenario_compliance(partner, scenario)
print(f"\nGemini's Compliance Analysis for {partner} Scenario:")
print(to_markdown(analysis))