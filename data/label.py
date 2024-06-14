import pandas as pd
import re
import time
import google.auth
import google.generativeai as genai

pattern = r':\s*([0-2])'
pattern_text = r'\b(\w+)\s*:'

# inputan nama file dan jumlah data yang dilabeli
nama_file = input ("Masukkan nama file CSV, contoh dataset.csv:\n")
range_awal = int(input ("Masukkan range awal, contoh 0: "))
range_akhir = int(input ("Masukkan range akhir, contoh 1000: "))
api_key = input ("Masukkan API key Google AI Studio: ")

df = pd.read_csv(nama_file)
df_copy = df.copy()
genai.configure(api_key=api_key)

def get_label(text):
 model = genai.GenerativeModel('gemini-1.5-flash')
 input_text = f"Labellah review berikut: '{text}' \nDengan ketentuan 0=negatif, 1=netral, 2=positif.\nContoh:\nfood : 0, service : 1, ambience : 0, price : 2\njika tidak disebutkan maka anggap saja 1/netral. Untuk aspect pada labelnya hanya 4 saja, yaitu food, service, ambience, price. Serta keterangan setelah labelnya tidak perlu"
 response = model.generate_content(input_text)
 resp = response.text
 return resp

reviews = []
food = []
service = []
ambiance = []
price = []
resp_text = []

error_label= []
input_error_label = []
output_error_label = []


for i in range(range_awal, range_akhir):
 print(f"Iterasi ke - {i}")
 text = df["reviews"][i]
 respon = get_label(text)
 print(respon)
 categories = re.findall(pattern_text, respon)
 categories = [category.lower() for category in categories]
 numbers = re.findall(pattern, respon)
 numbers = list(map(int, numbers))
 if len(numbers) == 4 and len(categories) == 4:
  try:
   food_index = categories.index("food")
   service_index = categories.index("service")
   ambiance_index = categories.index("ambience")
   price_index = categories.index("price")
  except:
   error_label.append(i)
   input_error_label.append(text)
   output_error_label.append(respon)
   continue
  resp_text.append(respon)
  reviews.append(text)
  food.append(int(numbers[food_index]))
  service.append(int(numbers[service_index]))
  ambiance.append(int(numbers[ambiance_index]))
  price.append(int(numbers[price_index]))
 else:
  error_label.append(i)
  input_error_label.append(text)
  output_error_label.append(respon)



df_array0 = pd.DataFrame({'reviews': reviews})
df_array1 = pd.DataFrame({'food': food})
df_array2 = pd.DataFrame({'service': service})
df_array3 = pd.DataFrame({'ambience': ambiance})
df_array4 = pd.DataFrame({'price': price})
df_array5 = pd.DataFrame({'resptext': resp_text})
# Menggabungkan DataFrame
df_combined = pd.concat([df_array0, df_array1, df_array2, df_array3, df_array4, df_array5], axis=1)

df_error1 = pd.DataFrame({'row_error': error_label})
df_error2 = pd.DataFrame({'input_error': input_error_label})
df_error3 = pd.DataFrame({'output_error': output_error_label})

df_error = pd.concat([df_error1, df_error2, df_error3], axis=1)

# Menyimpan DataFrame gabungan ke dalam file CSV dengan nama menyesuaikan
df_combined.to_csv(f'combined_dataset_{range_awal}_to_{range_akhir}.csv', index=False)
df_error.to_csv(f'error_dataset_{range_awal}_to_{range_akhir}.csv', index=False)

print(f"CSV file telah dibuat: combined_dataset_{range_awal}_to_{range_akhir}.csv")
