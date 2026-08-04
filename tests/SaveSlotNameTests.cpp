#include "save/SaveSlotName.hpp"

#include <iostream>
#include <string>

namespace {
bool expect(bool condition, const char *message)
{
    if (!condition) {
        std::cerr << message << '\n';
    }
    return condition;
}
}

int main()
{
    bool passed = true;
    passed &= expect(save_slot::isValidSlot(1), "Слот 1 отклонён");
    passed &= expect(save_slot::isValidSlot(10), "Слот 10 отклонён");
    passed &= expect(!save_slot::isValidSlot(0), "Слот 0 принят");
    passed &= expect(!save_slot::isValidSlot(11), "Слот 11 принят");

    passed &= expect(
        save_slot::sanitizeName("  Моя   игра Ё  ") == "Моя игра Ё",
        "Пробелы в имени обработаны неверно"
    );
    passed &= expect(
        save_slot::sanitizeName("Тест\n\tимени") == "Тестимени",
        "Управляющие символы не удалены"
    );

    std::string utf8Name = "Ёж";
    save_slot::removeLastUtf8Character(utf8Name);
    passed &= expect(
        utf8Name == "Ё",
        "Удаление последнего символа UTF-8 повреждает строку"
    );
    save_slot::removeLastUtf8Character(utf8Name);
    passed &= expect(
        utf8Name.empty(),
        "Последний символ UTF-8 не удалён"
    );

    std::string longName;
    for (int index = 0; index < 60; ++index) {
        longName += "Я";
    }
    const std::string shortened = save_slot::sanitizeName(longName);
    passed &= expect(
        shortened.size() == save_slot::MaximumNameBytes,
        "Ограничение длины имени работает неверно"
    );
    passed &= expect(
        shortened.substr(shortened.size() - 2) == "Я",
        "Ограничение длины разорвало символ UTF-8"
    );

    return passed ? 0 : 1;
}
