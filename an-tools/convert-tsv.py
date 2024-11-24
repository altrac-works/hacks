source_code = None

lines = []

with open("todo.tsv") as f:
    for line in f:
        fields = line.strip().split("\t")
        if len(fields) == 1:
            if fields[0].startswith("SOURCE"):
                source_code = fields[0].split("=")[1]
            continue

        name = fields[0]
        if " " in name:
            names = name.split()
            first_name = " ".join(names[:-1])
            last_name = names[-1]
        else:
            first_name = name
            last_name = None

        email = fields[1]
        zip = fields[2]

        phone = None
        if len(fields) > 3:
            phone = fields[3]

        volunteer = False
        if len(fields) > 4:
            volunteer = "1" in fields[4]

        affiliation = None
        if len(fields) > 5:
            affiliation = fields[5]

        cfields = [
            f"user_first_name={first_name}",
            f"user_zip_code={zip}",
            f"user_email={email}",
            f"search_user_field={email}",
        ]

        if last_name:
            cfields.append(f"user_last_name={last_name}")

        if phone:
            cfields.append(f"form-phone={phone}")

        if affiliation:
            cfields.append("custom_fields_NEW_ITEM_1_key=org_affiliation")
            cfields.append(f"custom_fields_NEW_ITEM_1_value={affiliation}")

        if source_code:
            cfields.append(f"source_code_source_code={source_code}")

        if volunteer:
            print("!!! VOLUNTEER !!!")

        print(";".join(cfields))
