# import gradio as gr
import pandas as pd
from datetime import timedelta
import datetime

df = pd.read_csv("/content/drive/MyDrive/file2.csv")
# a = df.duplicated('Name')
df2 = df.drop_duplicates('Name')

df2

def op_menu():
  print("Search Books")
  print('1. By Category')
  print('2. By Author')
  print('3. Receipt')
  print('4. Stop')
  print('5. Return')

# drop()
selected_df = pd.DataFrame()
def purchase_book(user_sub_category, selected_df = selected_df):
  # global mt_df
  flag1 = True

  while flag1:
    try:
      book_sno = int(input("Enter the serial number of your book to make purchase "))
      # flag1 = False
      if df2['Quantity'][book_sno] == 0:
        print("Sorry, this book isn't available")
        flag1 = True

      if user_sub_category == '1':
        sorted_purchase = sorted_non_fiction.loc[book_sno]
        flag1 = False
      elif user_sub_category == '2':
        sorted_purchase = sorted_fiction.loc[book_sno]
        flag1 = False
      elif user_sub_category == '3':
        sorted_purchase = sorted_author.loc[book_sno]
        flag1 = False
      selected_df = selected_df.append(sorted_purchase)
      df2['Quantity'][book_sno] = df2['Quantity'][book_sno] - 1

    except KeyError:
      print("Please enter valid serial number ")
      flag1 = True
    except ValueError:
      print("Valuerror")
      flag1 = True
    except UnboundLocalError:
      flag1 = True
  # mt_df = mt_df.drop(['User Rating', 'Reviews', 'Price', 'Year'], axis = 1)
  selected_df['Issued Date'] = pd.to_datetime('today').strftime("%d/%m/%Y")
  selected_df['Due Date'] = (pd.to_datetime('today') + timedelta(15)).strftime("%d/%m/%Y")
  return selected_df
# purchase_book(user_sub_category= '1')
# print(mt_df)

mt_df = pd.DataFrame()
con = True
while con:

  op_menu()
  main = []
  ask2 = True
  while ask2:
    try:
      category_of_user = input()
      ask2 = False
    except ValueError:
      ask2 = True
    except KeyError:
      ask2 = False
  if category_of_user == '1':

    print('1. Non Fiction')
    print('2. Fiction')
    ask3 = True
    while ask3:
      try:
        user_sub_category = input("Enter category of books you want to see ")
        ask3 = False
      except ValueError:
        ask3 = True
      except KeyError:
        ask3 = True

    group_genre = df2.groupby('Genre')
    #all non fiction books
    if user_sub_category == '1':
      grouping_non_fiction = group_genre.get_group('Non Fiction')
      sorted_non_fiction = grouping_non_fiction[['Name', 'Genre', 'Author']]
      print(sorted_non_fiction.to_string())
      ask_nonfiction = True
      while ask_nonfiction:
        # grouping_non_fiction = group_genre.get_group('Non Fiction')
        # sorted_non_fiction = grouping_non_fiction[['Name', 'Genre']]
        # print(sorted_non_fiction.to_string())
        # purchase_book(user_sub_category= '1')
        mt_df = mt_df.append(purchase_book(user_sub_category= '1'))
        print("You want to purchase more more non fiction section then press 1 else 0")
        continue_input = input()
        if continue_input == '0':
          ask_nonfiction = False
    #all fiction books
    elif user_sub_category == '2':
      grouping_fiction = group_genre.get_group('Fiction')
      sorted_fiction = grouping_fiction[['Name' , 'Genre', 'Author']]
      print(sorted_fiction.to_string())
      ask_fiction = True
      while ask_fiction:
        # purchase_book(user_sub_category= '2')
        mt_df = mt_df.append(purchase_book(user_sub_category= '2'))
        print("Do you want to purchase more fiction section? Then press 1 else 0")
        continue_input = input()
        if continue_input == '0':
          ask_fiction = False
    else:
      print("Unable to understand start again!!")


  #all author search
  elif category_of_user == '2':
    user_sub_category = '3'
    author_input_category = input("Enter the Author name: ").lower()
    group_author = df2.groupby(df['Author'].str.lower())
    grouping_author = group_author.get_group(author_input_category)
    sorted_author = grouping_author[['Name' , 'Genre', 'Author']]
    print(sorted_author.to_string())

    ask_author = True
    while ask_author:
      # purchase_book(user_sub_category='3')
      mt_df = mt_df.append(purchase_book(user_sub_category= '3'))

      print("Do you want to purchase more books from this section? Then press 1 else 0")
      continue_input = input()
      if continue_input == '0':
        ask_author = False

  elif category_of_user == '3':
    try:
     f = open('/content/drive/MyDrive/rey_lib_text.txt', 'w')
    except FileNotFoundError:
      print("No file is found!")
    for rec in mt_df.index:
      r1 = mt_df.loc[rec,'Name']
      r2 = mt_df.loc[rec, 'Author']
      r3 = mt_df.loc[rec,'Genre' ]
      r4 = mt_df.loc[rec, 'Issued Date']
      r5 = mt_df.loc[rec, 'Due Date']
      r6 = rec
      final_receipt = (f'Name:{r1}\nAuthor:{r2}\nGenre:{r3}\nIssued Date:{r4}\nDue Date:{r5}\nSerial_no:{r6}\n\n')
      f.write(final_receipt)
      print(final_receipt)
      con = False
    f.close()

  elif category_of_user == '4':
    con = False

  elif category_of_user == '5':
    print('How many books you want to return:- ')
    no_return = int(input())
    for k in range(no_return):
      print('Enter the S.no of book you want to return:- ')
      s_no_return = int(input())
      df2['Quantity'][s_no_return]  = df2['Quantity'][s_no_return] + 1



  else:
    print("Unable to understand strat again!!")
    con = False

df2