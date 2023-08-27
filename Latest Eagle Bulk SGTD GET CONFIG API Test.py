import json
import tkinter as tk
from tkinter import ttk, filedialog
import requests
import openpyxl
from datetime import datetime

API_Key = 'aznxXapJb8DI4X4NRnp0fVsoIvyUyvnX'
# Make the GET request
url = 'https://eaglebulk.pitstop.sgtradex.io/api/v1/config'
r_GET = requests.get(url, headers={'SGTRADEX-API-KEY': API_Key})

# Check the response
if r_GET.status_code == 200:
    print("Config Data retrieved successfully!")
    #print(r_GET.json())
else:
    print(f"Failed to get Config Data. Status code: {r_GET.status_code}")
    print(r_GET.text)    # Print the response content if the request was not successful

# Extract system IDs and names for consumes pilotage_service
consumes_list = r_GET.json()['data']['consumes']
produces_list = r_GET.json()['data']['produces']
system_ids_names = []

##===================PULL======================================
# for consume in consumes_list:
#     if consume['id'] == 'release_order':
#         from_list = consume['from']
#         for from_item in from_list:
#             system_ids_names.append((from_item['id'], from_item['name']))

#===================PUSH======================================
for produce in produces_list:
    if produce['id'] == 'manifest':
        to_list = produce['to']
        for to_item in to_list:
            system_ids_names.append((to_item['id'], to_item['name']))

# Print extracted system IDs and names
for system_id, system_name in system_ids_names:
    print(f"System ID: {system_id}, System Name: {system_name}")

def post_data():
    selected_index = combo_box.current()
    selected_id, selected_name = system_ids_names[selected_index]

    excel_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if excel_path:
        wb = openpyxl.load_workbook(excel_path)
        sheet = wb.active
        
        # Extract data from the Excel sheet
        data_rows = list(sheet.iter_rows(min_row=7, values_only=True))
        print(f"Data rows {data_rows}")
        # Replace 'YOUR_API_LICENSE_KEY' with your actual API license key
        API_Key = 'aznxXapJb8DI4X4NRnp0fVsoIvyUyvnX'

        # Replace 'API_ENDPOINT_URL' with the actual API endpoint URL where you want to post the data
        api_endpoint_url = 'https://eaglebulk.pitstop.sgtradex.io/api/v1'

        participants_id = selected_id
        participants_name = selected_name

        payload_entries = []
        manifest_lineitem = []
        for i in range(len(data_rows)):
            manifest_lineitem.append({
                    "po_no": data_rows[i][1],
                    "desc": data_rows[i][2],
                    "supplier": data_rows[i][3]  # Convert to integer
                })
        # Convert datetime to string before adding to the payload
        manifest_vessel_eta = sheet["C4"].value
        if isinstance(manifest_vessel_eta, datetime):
            manifest_vessel_eta_str = manifest_vessel_eta.isoformat()
        else:
            manifest_vessel_eta_str = manifest_vessel_eta

        payload_entries.append({
            "manifest_vessel_nm": sheet["C2"].value,
            "manifest_vessel_destination": sheet["C3"].value,
            "manifest_vessel_eta": manifest_vessel_eta_str,
            "manifest_vessel_remarks": "",
            "manifest_agent": "",
            "manifest_lighter_operator": "",
            "manifest_agent": "",
            "manifest_no": "",
            "manifest_lineitem": manifest_lineitem,
            "attachments": [
                {
                "filename": "",
                "file_content": ""
                }
                ]
             # Assuming release dates are in the last 3 columns
        })
        on_behalf_of_id = "f9345af0-0b1d-4ff5-8c7b-a953868c4fbd"

        payload = {
            "participants": [{
                "id": participants_id,
                "name": participants_name,
                "meta": {"data_ref_id": ""}
            }],
            "payload": payload_entries,
            "on_behalf_of": [{"id": on_behalf_of_id}]
        }
        print(f"Final Payload {payload}")

        json_string = json.dumps(payload, indent=4)  # Convert payload dictionary to JSON string
        # Rest of the code to send the JSON payload to the API
        data=json.loads(json_string)
        print(data)
        # # Make the POST request
        # response = requests.post("https://eaglebulk.pitstop.sgtradex.io/api/v1/data/push/release_order", json=data, headers={'SGTRADEX-API-KEY': API_Key})

        # # Check the response
        # if response.status_code == 200:
        #     print("Data posted successfully!")
        #     print(response.json())  # If the API returns any data in the response, you can access it using .json()
        # else:
        #     print(f"Failed to post data. Status code: {response.status_code}")
        #     print(response.text)    # Print the response content if the request was not successful

# Create the main window
root = tk.Tk()
root.title("System Selection")

# Create a label
label = tk.Label(root, text="Select a Participant to PUSH Pilotage Service:")
label.pack(padx=10, pady=10)

# Create a combobox to select the system
combo_box = ttk.Combobox(root, values=[name for id, name in system_ids_names], width=70)
combo_box.pack(padx=10, pady=5)

# Create a label to display the selected system
result_label = tk.Label(root, text="")
result_label.pack(padx=10, pady=5)

post_button = tk.Button(root, text="Post Data", command=post_data)
post_button.pack(padx=10, pady=10)

# Start the GUI event loop
root.mainloop()