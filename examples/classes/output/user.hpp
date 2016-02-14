/**
 * \file user.hpp
 */

#pragma once

#include <string>

class User {
public:
    User(int age, std::string name) :
        m_age(age),
        m_name(name)
    {}

    int getAge() const {
        return m_age;
    }

    void setAge(int age) {
        m_age = age;
    }
    std::string getName() const {
        return m_name;
    }

    void setName(std::string name) {
        m_name = name;
    }

private:
    int m_age;
    std::string m_name;
};
