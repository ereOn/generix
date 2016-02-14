/**
 * \file user_account.hpp
 */

#pragma once

#include <string>

class UserAccount {
public:
    UserAccount(int id) :
        m_id(id)
    {}

    int getId() const {
        return m_id;
    }

    void setId(int id) {
        m_id = id;
    }

private:
    int m_id;
};
