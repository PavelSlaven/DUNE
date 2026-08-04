#include "save/SaveFileCodec.hpp"

#include <iostream>
#include <string>

namespace {
bool expectFailure(
    std::string_view name,
    std::string_view contents,
    int version,
    std::size_t maximumBytes)
{
    const save_file::DecodeResult result =
        save_file::decode(contents, version, maximumBytes);
    if (!result.succeeded()) {
        return true;
    }
    std::cerr << name << ": повреждённый файл был принят\n";
    return false;
}
}

int main()
{
    constexpr int version = 1;
    const std::string body =
        "META 0 1 0\n"
        "TEXT Проверка Ёжик\n"
        "END\n";
    const std::string encoded = save_file::encode(body, version);
    const save_file::DecodeResult decoded =
        save_file::decode(encoded, version, 1024);

    bool passed = true;
    if (!decoded.succeeded() || decoded.body != body) {
        std::cerr << "Корректное сохранение не прошло круговой тест\n";
        passed = false;
    }

    std::string corrupted = encoded;
    corrupted.back() ^= 1;
    passed &= expectFailure(
        "Контрольная сумма",
        corrupted,
        version,
        1024
    );
    passed &= expectFailure(
        "Версия",
        encoded,
        version + 1,
        1024
    );
    passed &= expectFailure(
        "Заголовок",
        "D2TM_SAVE",
        version,
        1024
    );
    passed &= expectFailure(
        "Ограничение размера",
        encoded,
        version,
        4
    );

    return passed ? 0 : 1;
}
