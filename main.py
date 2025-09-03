import src.openfda as openfda

def pretty_print(drug: str, sections: dict):
    print(f"\n=== {drug}: label excerpts ===")
    if not sections:
        print("No FDA label found.")
        return
    if sections.get("drug_interactions"):
        print("\n[Drug Interactions]")
        txt = sections["drug_interactions"]
        print(txt[:1200] + ("..." if len(txt) > 1200 else ""))
    if sections.get("warnings_and_cautions"):
        print("\n[Warnings and Cautions]")
        txt = sections["warnings_and_cautions"]
        print(txt[:800] + ("..." if len(txt) > 800 else ""))
    if sections.get("warnings"):
        print("\n[Warnings]")
        txt = sections["warnings"]
        print(txt[:600] + ("..." if len(txt) > 600 else ""))
    if sections.get("precautions"):
        print("\n[Precautions]")
        txt = sections["precautions"]
        print(txt[:600] + ("..." if len(txt) > 600 else ""))

def run_cli():
    print("Drug Interaction Checker (openFDA labels)")
    d1 = input("Enter first drug name: ").strip()
    d2 = input("Enter second drug name: ").strip()

    s1 = openfda.get_interaction_text(d1)
    s2 = openfda.get_interaction_text(d2)

    pretty_print(d1, s1)
    pretty_print(d2, s2)

    notes = openfda.simple_crosscheck(d1, d2)
    print("\n=== Cross-mention check ===")
    if notes:
        for n in notes:
            print(" - " + n)
    else:
        print("No explicit cross-mentions found in 'Drug Interactions' sections.")

if __name__ == "__main__":
    run_cli()
