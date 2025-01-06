from constants import *
class GoogleSheets():
    def __init__(self):
        #self.color = color
        #self.sheet_name = sheet_name
        #self.StartRowIndex = StartRowIndex
        #self.EndRowIndex = EndRowIndex
        #self.StartColumnIndex = StartColumnIndex
        self.file = find_file("nea-project-395311-334f9063e146.json")
        self.sa = gspread.service_account(filename=self.file)
        self.sh = self.sa.open('Part of NEA Project')
        self.wks = self.sh.worksheet('Sheet1')
        self.scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.file, self.scope)
        self.service = build("sheets", "v4", credentials=self.credentials,static_discovery=False)
        self.spreadsheet_ID = "1fpAaccYnntwLTYlrisJ9MieJtKLAhSFi8kUdPG8QMQ8"
        self.sheet_ID = 0
        self.basics()
        #self.delete_sheet()
        #self.create_chart()
        #self.create_chart_two()
        #self.download()  
    def basics(self):

        #self.wks.clear()
        # Update a cell
        #values_to_update = [["Name","ID", "PR_weight", "Rep_weight", "Reps", "Sets"]]

        #self.wks.update('A1:F1', values_to_update)
    

        #call = c.execute('''SELECT name,ID,PR_weight,Rep_weight,reps,sets FROM Exercise''').fetchall()
        '''
        vals = []
        vals = vals[147:len(vals)]
        for i in call:
          cur = [i[0], i[1], i[2], i[3], i[4],i[5]]
          vals.append(cur)  
        print(vals)
        batch_size = 10  # Number of rows per batch
        delay_seconds = 5  # Delay in seconds betwee  n batches

        for i in range(132, len(vals), batch_size):
            batch = vals[i:i + batch_size]
            for row in batch:
                current = [row[0], row[1], row[2], row[3], row[4],row[5]]
                update_range = f"A{vals.index(row)+2}:F{vals.index(row)+2}"
                self.wks.update(update_range, [current])
            time.sleep(delay_seconds)  # Introduce a delay between batches
        '''
    def delete_sheet(self):
      spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_ID).execute()
      sheets = spreadsheet['sheets']

      # Find the sheet ID based on the sheet name
      sheet_id_to_delete = None
      for sheet in sheets:
          if sheet['properties']['title'] == self.sheet_name:
              sheet_id_to_delete = sheet['properties']['sheetId']
              break

      if sheet_id_to_delete is None:
          print(f'Sheet "{sheet_name_to_delete}" not found in the spreadsheet')
      else:
          # Construct the request body to delete the sheet
          request_body = {
              'requests': [
                  {
                      'deleteSheet': {
                          'sheetId': sheet_id_to_delete
                      }
                  }
              ]
          }

          # Execute the batchUpdate request to delete the sheet
          response = self.service.spreadsheets().batchUpdate(
              spreadsheetId=self.spreadsheet_ID,
              body=request_body
          ).execute()

          print(f'Sheet "{self.sheet_name}" deleted successfully')
    def download(self):
      client = gspread.authorize(self.credentials)
      spreadsheet = client.open_by_key(self.spreadsheet_ID)

      # Download the spreadsheet data as an Excel file
      output_path = r"C:\Users\khait\Downloads\sheet.xlsx"
      spreadsheet.get_worksheet(0).export(output_path)

      print(f'Spreadsheet downloaded to {output_path}')
    def create_chart(self):
        add_sheet_request = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": self.sheet_name,
                        }
                    }
                }
            ]
        }

        # Execute the request to add a new sheet
        response = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_ID,
            body=add_sheet_request
        ).execute()

        # The response will contain information about the added sheet
        new_sheet_properties = response.get("replies")[0].get("addSheet").get("properties")

        # Use the sheet ID of the newly added sheet in your chart creation
        new_sheet_ID = new_sheet_properties.get("sheetId")

        data_range = "B2:C9"
        request_body = {
            'requests': [
                {
                    'addChart': {
                        'chart': {
                            'spec': {
                                'title': 'Trial chart from Python',
                                'basicChart': {
                                    'chartType': 'line',
                                    'legendPosition': 'BOTTOM_LEGEND',
                                    'axis': [
                                        {
                                            'position': 'RIGHT_AXIS',
                                            'title': str(self.wks.cell(1, self.StartColumnIndex).value),
                                        },
                                        {
                                            'position': 'LEFT_AXIS',
                                            'title': str(self.wks.cell(1, self.StartColumnIndex + 1).value),
                                        },
                                        {
                                            'position': 'BOTTOM_AXIS',
                                            'title': 'Exercise with ID (^) {find name in table}',
                                        },
                                    ],
                                    "domains": [
                                        {
                                            "domain": {
                                                "sourceRange": {
                                                    "sources": [
                                                        {
                                                            "sheetId": self.sheet_ID,
                                                            "startRowIndex": self.StartRowIndex + 1,
                                                            "endRowIndex": self.EndRowIndex,
                                                            "startColumnIndex": 0,
                                                            "endColumnIndex": 1
                                                        }
                                                    ]
                                                }
                                            }
                                        }
                                    ],
                                    'series': [                                 {
                                            'series': {
                                                'sourceRange': {
                                                    'sources': [
                                                        {
                                                            'sheetId': self.sheet_ID,
                                                            'startRowIndex': self.StartRowIndex + 1,
                                                            'endRowIndex': self.EndRowIndex,
                                                            'startColumnIndex': self.StartColumnIndex-1,
                                                            'endColumnIndex': self.StartColumnIndex,
                                                        },
                                                    ],
                                                },
                                            },
                                            'targetAxis': 'LEFT_AXIS',
                                        },

                                        {
                                            'series': {
                                                'sourceRange': {
                                                    'sources': [
                                                        {
                                                            'sheetId': self.sheet_ID,
                                                            'startRowIndex': self.StartRowIndex + 1,
                                                            'endRowIndex': self.EndRowIndex,
                                                            'startColumnIndex': self.StartColumnIndex,
                                                            'endColumnIndex': self.StartColumnIndex+1,
                                                        },
                                                    ],
                                                },
                                            },
                                            'targetAxis': 'RIGHT_AXIS',
                                        },
                                    ],
                                }
                            },
                            "position": {
                                "overlayPosition": {
                                    "anchorCell": {
                                        "sheetId": new_sheet_ID,
                                        "rowIndex": 0,
                                        "columnIndex": 2
                                    },
                                    "offsetXPixels": 0,
                                    "offsetYPixels": 0
                                }
                            }
                        }
                    }
                }
            ]
        }
        non_empty_values_count = sum(1 for cell in self.wks.range('A2:A200') if cell.value)
        row = 2
        # Execute the batchUpdate request to create the chart
        response2 = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_ID,
            body=request_body,
        ).execute()
        print('Chart created successfully')
    def create_chart_two(self):
        add_sheet_request = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": self.sheet_name,
                        }
                    }
                }
            ]
        }

        # Execute the request to add a new sheet
        response = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_ID,
            body=add_sheet_request
        ).execute()

        # The response will contain information about the added sheet
        new_sheet_properties = response.get("replies")[0].get("addSheet").get("properties")

        # Use the sheet ID of the newly added sheet in your chart creation
        new_sheet_ID = new_sheet_properties.get("sheetId")

        data_range = "B2:C9"
        request_body = {
            'requests': [
                {
                    'addChart': {
                        'chart': {
                            'spec': {
                                'title': 'Trial chart from Python',
                                'basicChart': {
                                    'chartType': 'line',
                                    'legendPosition': 'BOTTOM_LEGEND',
                                    'axis': [
                                        {
                                            'position': 'RIGHT_AXIS',
                                            'title': str(self.wks.cell(1, self.StartColumnIndex).value),
                                        },
                                        {
                                            'position': 'LEFT_AXIS',
                                            'title': str(self.wks.cell(1, self.StartColumnIndex + 1).value),
                                        },
                                        {
                                            'position': 'BOTTOM_AXIS',
                                            'title': 'Exercise with ID (^) {find name in table}',
                                        },
                                    ],
                                    "domains": [
                                        {
                                            "domain": {
                                                "sourceRange": {
                                                    "sources": [
                                                        {
                                                            "sheetId": self.sheet_ID,
                                                            "startRowIndex": self.StartRowIndex + 1,
                                                            "endRowIndex": self.EndRowIndex,
                                                            "startColumnIndex": 0,
                                                            "endColumnIndex": 1
                                                        }
                                                    ]
                                                }
                                            }
                                        }
                                    ],
                                    'series': []
                                }
                            },
                            "position": {
                                "overlayPosition": {
                                    "anchorCell": {
                                        "sheetId": new_sheet_ID,
                                        "rowIndex": 0,
                                        "columnIndex": 2
                                    },
                                    "offsetXPixels": 0,
                                    "offsetYPixels": 0
                                }
                            }
                        }
                    }
                }
            ]
        }

        num = sum(1 for cell in self.wks.range('A2:A200') if cell.value)
        row = 2
        print(num)
        all_series = []
        for i in range(row, num):
            self.StartRowIndex = i + row
            self.EndRowIndex = i + row + 1
            data_left = {
                'series': {
                    'sourceRange': {
                        'sources': [
                            {
                                'sheetId': self.sheet_ID,
                                'startRowIndex': row + 1,
                                'endRowIndex': row + 2,
                                'startColumnIndex': self.StartColumnIndex - 1,
                                'endColumnIndex': self.StartColumnIndex
                            }
                        ]
                    },
                },
                'targetAxis': 'LEFT_AXIS',
                'lineStyle': {
                'type': 'SOLID'
                }
            }
            data_right = {
                'series': {
                    'sourceRange': {
                        'sources': [
                            {
                                'sheetId': self.sheet_ID,
                                'startRowIndex': row + 1,
                                'endRowIndex': row + 2,
                                'startColumnIndex': self.StartColumnIndex,
                                'endColumnIndex': self.StartColumnIndex + 1
                            }
                        ]
                    },
                },
                'targetAxis': 'RIGHT_AXIS',
                'lineStyle': {
                'type': 'SOLID'
                }
            }
            all_series.append(data_left)
            all_series.append(data_right)



        # Update the series data in the request body
        request_body['requests'][0]['addChart']['chart']['spec']['basicChart']['series'] = all_series

        # Execute the batchUpdate request to create the chart with multiple series
        response = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_ID,
            body=request_body,
        ).execute()

        print('Chart created successfully')

'''
Chart1 = GoogleSheets('blue','Rep weight against reps',2,146,3)
Chart2 = GoogleSheets('green','PR weight against reps',2,146,5)
Chart3 = GoogleSheets('red','Reps against sets',2,146,6)
def Callback():
  def call(url):
    webbrowser.open_new(url)  
  def call2(url2):    
    webbrowser.open_new(url2)
  link1 = tk.Label(tab_search("Hyperlinks"), text="NEA Chart", fg="blue", cursor="hand2",font=("Helvetica",25))
  link1.pack()
  link1.bind("<Button-1>", lambda e: call("https://docs.google.com/spreadsheets/d/1PCYPD-uY5DGtHUtNi77uNN08u8dv5moiLeAZY8U7RF0/edit#gid=0"))
  link2 = tk.Label(tab_search("Hyperlinks"), text="Replit equivalent code", fg="blue", cursor="hand2",font=("Helvetica",25))
  link2.pack()
  link2.bind("<Button-1>", lambda e: call2("https://replit.com/@ArmaanKHAITAN/Project-file"))
  
Callback()



    header_row = self.wks.row_values(1)
    columns = self.my_tree["columns"]
    google_sheets_updateables = {"name":None,"ID":None,"Rep_weight":None,"reps":None,"PR_weight":None,"reps":None,"sets":None}


    for val in new_attributes:
      index = new_attributes.index(val)
      for key,value in google_sheets_updateables.items():
        if columns[index] == key:
          google_sheets_updateables[key] = val

    for key in google_sheets_updateables:
      if key == "sets":
          google_sheets_updateables[key] = existing_attributes[columns.index("sets")]


    google_sheets_updateables_list = list(google_sheets_updateables.values())
    rep_weight_index = columns.index("Rep_weight")
    google_sheets_updateables_list[2]=existing_attributes[rep_weight_index]
    google_sheets_updateables_list.insert(5,google_sheets_updateables_list[3])


    for i in range(1, len(google_sheets_updateables_list)):
      value = google_sheets_updateables_list[i]
      if '.' in str(value):
        google_sheets_updateables_list[i] = float(value)
      else:
        google_sheets_updateables_list[i] = int(value)

    #print(google_sheets_updateables_list)
    ID_to_update = int(google_sheets_updateables_list[1])
    row_idx_to_update = None
    values = self.wks.get_all_values()

    for row_idx, row in enumerate(values):
      if row[1] != 'ID':
        if int(row[1]) == ID_to_update:
          row_idx_to_update = row_idx
          break
      else:
        continue
    if row_idx_to_update is not None:
        global update_values
        update_values = [google_sheets_updateables_list]

        update_range = f"A{row_idx_to_update + 1}:G{row_idx_to_update + 1}"
        self.wks.update(update_range, update_values)
        print(update_values)
        #print("Successfully updated")
    else:
        print(f"Row with name '{ID_to_update}' not found")
'''
