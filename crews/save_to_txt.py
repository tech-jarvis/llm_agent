# Step 4: Save all information to a .txt file
def save_to_txt(file_name, content):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)