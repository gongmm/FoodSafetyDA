def cut_file():
    with open("data/food.train", "r", encoding="utf-8") as food_dev_file:
        with open("data/new_food.train", "a+", encoding="utf-8") as write_file:
            write_file.truncate()
            begin_line = 0
            end_line = 0
            for line in food_dev_file:
                end_line += 1
                first_char = line[0]
                write_file.writelines(line)
                if (first_char == "。" or first_char == "，" or first_char == "？") and end_line - begin_line > 20:
                    begin_line = 0
                    end_line = 0
                    write_file.writelines("\n")

                print(first_char)


if __name__ == "__main__":
    cut_file()
