import pandas as pd
import re
import google.auth
import google.generativeai as genai

# Pola regex untuk ekstraksi label
pattern = r':\s*([0-2])'
pattern_text = r'\b(\w+)\s*:'

# Fungsi untuk mendapatkan label dari model Generative AI
def get_label(text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    input_text = (f"Labellah review berikut: '{text}' \nDengan ketentuan 0=negatif, 1=netral, 2=positif.\n"
                  "Contoh:\nfood : 0, service : 1, ambience : 0, price : 2\n"
                  "jika tidak disebutkan maka anggap saja 1/netral. "
                  "Untuk aspect pada labelnya hanya 4 saja, yaitu food, service, ambience, price. "
                  "Serta keterangan setelah labelnya tidak perlu")
    response = model.generate_content(input_text)
    return response.text

# Fungsi untuk memproses setiap review dan mengumpulkan hasilnya
def process_reviews(df, start, end):
    reviews, food, service, ambiance, price, resp_text = [], [], [], [], [], []
    error_label, input_error_label, output_error_label = [], [], []

    for i in range(start, end):
        print(f"Iterasi ke - {i}")
        text = df["reviews"][i]
        try:
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
                food.append(numbers[food_index])
                service.append(numbers[service_index])
                ambiance.append(numbers[ambiance_index])
                price.append(numbers[price_index])
            else:
                error_label.append(i)
                input_error_label.append(text)
                output_error_label.append(respon)
        except:
            print(f"Error respon iterasi ke - {i}")
            continue

    return reviews, food, service, ambiance, price, resp_text, error_label, input_error_label, output_error_label

# Fungsi untuk menyimpan hasil ke file CSV
def save_to_csv(data, error_data, start, end):
    df_reviews = pd.DataFrame({'reviews': data[0]})
    df_food = pd.DataFrame({'food': data[1]})
    df_service = pd.DataFrame({'service': data[2]})
    df_ambiance = pd.DataFrame({'ambience': data[3]})
    df_price = pd.DataFrame({'price': data[4]})
    df_resp_text = pd.DataFrame({'resptext': data[5]})
    
    df_combined = pd.concat([df_reviews, df_food, df_service, df_ambiance, df_price, df_resp_text], axis=1)
    df_combined.to_csv(f'combined_dataset_{start}_to_{end}.csv', index=False)
    
    df_error = pd.DataFrame({'row_error': error_data[0], 'input_error': error_data[1], 'output_error': error_data[2]})
    df_error.to_csv(f'error_dataset_{start}_to_{end}.csv', index=False)
    
    print(f"CSV file telah dibuat: combined_dataset_{start}_to_{end}.csv")

# Main script
if __name__ == "__main__":
    nama_file = input("Masukkan nama file CSV, contoh dataset.csv:\n")
    range_awal = int(input("Masukkan range awal, contoh 0:"))
    range_akhir = int(input("Masukkan range akhir, contoh 1000:"))
    
    df = pd.read_csv(nama_file)
    genai.configure(api_key="APIKey dari Google AI Studio") # input apikey dari Google AI Studio
    
    results = process_reviews(df, range_awal, range_akhir)
    data = results[:6]
    error_data = results[6:]
    save_to_csv(data, error_data, range_awal, range_akhir)

