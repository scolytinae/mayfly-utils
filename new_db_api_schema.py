#!/usr/bin/env python

import re
import subprocess

schemas = [
    'schema_api_00_02', 
    'schema_api_00_02_private'
]
rName = re.compile("-- Name: .*")
r = re.compile("-- Name: (FUNCTION )?(.*?)(\\(.*?\\))")
rFunc = re.compile("create function (.*?)(\\(.*?\\))", re.IGNORECASE)


mac_head = '''---
--- добавление доменам maclabels
---
set search_path = coretype;

'''

mac_func_head = "-- {}"

mac_sec_definer = '''
alter 
{}
security definer;
'''

mac_label = '''
mac label on 
{}
is '{{0,0}}';


'''

def split_functions(schema, num):
    with open(f"{schema}.sql", 'r') as f:
        in_lines = f.readlines()

    func_name = ""    
    out_lines = []
    for line in in_lines:        
        # if line.strip() == "--":
        #     continue

        line = line.replace("schema_api_00_02", "schema_api_00_03")

        m = r.match(line)
        if m:
            new_func_name = m.group(2)
            if (not func_name):
                out_lines = ["--\n", line]
            elif ((func_name == new_func_name)):
                out_lines.append(line)
            elif func_name and len(out_lines) > 0:
                print (f"Write new function: {new_func_name}")
                with open(f"namedb_0047_{str(num).zfill(4)}_{func_name}.sql", "w+") as fo:
                    out_lines = out_lines[:-1]
                    out_lines.append("/* E O F */\n")
                    fo.writelines(out_lines)
                    out_lines = ["--\n", line]
                    num += 1
            
            func_name = new_func_name
        
        else:
            if (rName.match(line) and func_name and len(out_lines) > 1):
                print (f"Write new function: {func_name}")
                with open(f"namedb_0047_{str(num).zfill(4)}_{func_name}.sql", "w+") as fo:
                    out_lines = out_lines[:-1]
                    out_lines.append("/* E O F */\n")
                    fo.writelines(out_lines)
                    out_lines = ["--\n", line]
                    num += 1
                func_name = ""
                out_lines.clear()
            else:
                out_lines.append(line)
    
    if (func_name and len(out_lines) > 1):
        print (f"Write new function: {func_name}")
        with open(f"namedb_0047_{str(num).zfill(4)}_{func_name}.sql", "w+") as fo:
            out_lines = out_lines[:-1]
            out_lines.append("/* E O F */\n")
            fo.writelines(out_lines)
            out_lines = ["--\n", line]
            num += 1

    return num


def make_defmacset(schema, num):
    with open(f"{schema}.sql", 'r') as f:
        in_lines = f.readlines()

    new_schema = schema.replace("schema_api_00_02", "schema_api_00_03")
    func_name = ""    
    out_lines = [mac_head]
    for line in in_lines:        
        line = line.replace("schema_api_00_02", "schema_api_00_03")

        m = rFunc.match(line)
        if m:
            new_func_name = new_schema + '.' + m.group(1) + m.group(2)
            if (func_name == new_func_name):
                continue

            print (new_func_name)
            func_name = new_func_name
            out_lines.append(mac_func_head.format(m.group(1)))
            out_lines.append(mac_sec_definer.format(func_name))
            out_lines.append(mac_label.format(func_name))

            num += 1            

    fname = "private_functions" if "private" in new_schema else "functions"

    with open(f"namedb_0047_0001_defmacsett_{fname}.sql", "w+") as fo:
        out_lines.append("/* E O F */\n")
        fo.writelines(out_lines)

    return num


if __name__ == "__main__":
    first_num = 2
    num = first_num
    for schema in schemas:
        done = subprocess.run([f"pg_dump --schema={schema} -d namedb -U postgres --no-owner -f {schema}.sql"], shell=True)
        if (not done):  
            print("Some subprocess error")
    
        # num = split_functions(schema, num)
        num = make_defmacset(schema, num)

    print(f"Generated {num - first_num} files")