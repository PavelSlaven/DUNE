#pragma once

#include <functional>
#include <string>
#include <utility>

class SaveGameFlow {
public:
    using SaveCallback = std::function<bool(int slot, const std::string &name, std::string &errorMessage)>;
    using LoadCallback = std::function<bool(int slot, std::string &errorMessage)>;
    using QuickCallback = std::function<bool(std::string &errorMessage)>;

    SaveGameFlow(SaveCallback save, LoadCallback load, QuickCallback quickSave, QuickCallback quickLoad)
        : m_save(std::move(save)),
          m_load(std::move(load)),
          m_quickSave(std::move(quickSave)),
          m_quickLoad(std::move(quickLoad)) {
    }

    bool save(int slot, const std::string &name, std::string &errorMessage) const {
        return m_save(slot, name, errorMessage);
    }

    bool load(int slot, std::string &errorMessage) const {
        return m_load(slot, errorMessage);
    }

    bool quickSave(std::string &errorMessage) const {
        return m_quickSave(errorMessage);
    }

    bool quickLoad(std::string &errorMessage) const {
        return m_quickLoad(errorMessage);
    }

private:
    SaveCallback m_save;
    LoadCallback m_load;
    QuickCallback m_quickSave;
    QuickCallback m_quickLoad;
};
