#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <string>
#include <tuple>

using namespace std;

map<string, int> condition_codes = {
    {"LT", 1},
    {"LE", 2},
    {"EQ", 3},
    {"GT", 4},
    {"GE", 5},
    {"ANY", 6}
};

map<string, int> register_codes = {
    {"AREG", 1},
    {"BREG", 2},
    {"CREG", 3},
    {"DREG", 4}
};

map<string, tuple<string, int>> mnemonics = {
    {"STOP", {"IS", 0}},
    {"ADD", {"IS", 1}},
    {"SUB", {"IS", 2}},
    {"MULT", {"IS", 3}},
    {"MOVER", {"IS", 4}},
    {"MOVEM", {"IS", 5}},
    {"COMP", {"IS", 6}},
    {"BC", {"IS", 7}},
    {"DIV", {"IS", 8}},
    {"READ", {"IS", 9}},
    {"PRINT", {"IS", 10}},
    {"START", {"AD", 1}},
    {"END", {"AD", 2}},
    {"ORIGIN", {"AD", 3}},
    {"EQU", {"AD", 4}},
    {"LTORG", {"AD", 5}},
    {"DC", {"DL", 1}},
    {"DS", {"DL", 2}}
};

vector<pair<string, int>> symtab;

int find_symbol(const string& symbol_name) {
    for (size_t i = 0; i < symtab.size(); ++i) {
        if (symtab[i].first == symbol_name) return i;
    }
    return -1;
}

int update_symbol(const string& symbol_name, int addr) {
    for (size_t i = 0; i < symtab.size(); ++i) {
        if (symtab[i].first == symbol_name) {
            if (addr != -1) {
                symtab[i].second = addr;
            }
            return i;
        }
    }
    symtab.push_back(make_pair(symbol_name, addr));
    return symtab.size() - 1;
}

vector<pair<string, int>> lit_tab(10, make_pair("", -1));
vector<int> pool_tab(10, -1);
int lit_tab_ptr = 0;
int pool_tab_ptr = 0;
int location_cntr = 1;

void init_literals() {
    for (int i = pool_tab[pool_tab_ptr]; i < lit_tab_ptr; ++i) {
        lit_tab[i].second = location_cntr;
        ++location_cntr;
    }
    ++pool_tab_ptr;
    pool_tab[pool_tab_ptr] = lit_tab_ptr;
}

int main() {
    pool_tab[pool_tab_ptr] = 0;
    string source_file_path;
    cout << "Enter source code file path: ";
    cin >> source_file_path;

    ifstream file(source_file_path);
    if (!file.is_open()) {
        cerr << "Error: Could not open " << source_file_path << endl;
        return 1;
    }

    vector<string> source_lines;
    string line;
    while (getline(file, line)) {
        source_lines.push_back(line);
    }
    file.close();

    vector<vector<string>> source_line_tokens;
    for (const string& line : source_lines) {
        istringstream iss(line);
        vector<string> tokens;
        string token;
        while (iss >> token) {
            tokens.push_back(token);
        }
        source_line_tokens.push_back(tokens);
    }

    vector<string> ic_lines;

    for (const auto& line_tokens : source_line_tokens) {
        string label = "", mnemonic_str = "", operand1 = "", operand2 = "";

        if (mnemonics.count(line_tokens[0])) {
            mnemonic_str = line_tokens[0];
            if (line_tokens.size() == 2) operand1 = line_tokens[1];
            if (line_tokens.size() == 3) {
                operand1 = line_tokens[1];
                operand2 = line_tokens[2];
            }
        } else {
            label = line_tokens[0];
            mnemonic_str = line_tokens[1];
            if (line_tokens.size() == 3) operand1 = line_tokens[2];
            if (line_tokens.size() == 4) {
                operand1 = line_tokens[2];
                operand2 = line_tokens[3];
            }
        }

        string mnemonic_class = get<0>(mnemonics[mnemonic_str]);
        int mnemonic_opcode = get<1>(mnemonics[mnemonic_str]);
        string ic_line = (mnemonic_class != "AD" ? to_string(location_cntr) : "   ") + " (" + mnemonic_class + "," + to_string(mnemonic_opcode) + ") ";

        if (mnemonic_class != "DL" && !label.empty()) {
            update_symbol(label, location_cntr);
        }

        if (mnemonic_str == "LTORG") {
            init_literals();
        }

        if (mnemonic_str == "START") {
            location_cntr = stoi(operand1);
            ic_line += "(C," + to_string(location_cntr) + ")";
        }

        if (mnemonic_str == "ORIGIN") {
            size_t pos = operand1.find_first_of("+-");
            if (pos != string::npos) {
                string symbol_name = operand1.substr(0, pos);
                int symbol_index = find_symbol(symbol_name);
                int symbol_addr = symbol_index != -1 ? symtab[symbol_index].second : 0;
                location_cntr = stoi(operand1.replace(pos, 1, "") + to_string(symbol_addr));
                ic_line += "(C," + to_string(location_cntr) + ")";
            } else {
                int symbol_index = find_symbol(operand1);
                location_cntr = symbol_index == -1 ? stoi(operand1) : symtab[symbol_index].second;
                ic_line += "(C," + to_string(location_cntr) + ")";
            }
        }

        if (mnemonic_str == "EQU") {
            size_t pos = operand1.find_first_of("+-");
            int updated_val = 0;
            if (pos != string::npos) {
                string symbol_name = operand1.substr(0, pos);
                int symbol_index = find_symbol(symbol_name);
                int symbol_addr = symbol_index != -1 ? symtab[symbol_index].second : 0;
                updated_val = stoi(operand1.replace(pos, 1, "") + to_string(symbol_addr));
                update_symbol(label, updated_val);
                ic_line += "(S," + to_string(symbol_index) + ") (C," + to_string(updated_val) + ")";
            } else {
                int symbol_index = find_symbol(operand1);
                updated_val = symbol_index == -1 ? stoi(operand1) : symtab[symbol_index].second;
                update_symbol(label, updated_val);
            }
        }

        if (mnemonic_class == "DL") {
            int symbol_index = update_symbol(label, location_cntr);
            if (mnemonic_str == "DC") {
                location_cntr += 1;
                operand1 = operand1.substr(1, operand1.size() - 2);
            } else if (mnemonic_str == "DS") {
                location_cntr += stoi(operand1);
            }
            ic_line += "(S," + to_string(symbol_index) + ") (C," + operand1 + ")";
        }

        if (mnemonic_class == "IS") {
            if (mnemonic_str == "READ" || mnemonic_str == "PRINT") {
                int symbol_index = update_symbol(operand1, -1);
                ic_line += "(S," + to_string(symbol_index) + ")";
            } else if (mnemonic_str == "BC") {
                int symbol_index = update_symbol(operand2, -1);
                ic_line += "(" + to_string(condition_codes[operand1]) + ") (S," + to_string(symbol_index) + ")";
            } else if (mnemonic_str == "STOP") {
                // STOP has no operands
            } else {
                if (operand2.find('=') != string::npos) {
                    string literal_val = operand2.substr(operand2.find('=') + 1);
                    ic_line += "(" + to_string(register_codes[operand1]) + ") (L," + to_string(lit_tab_ptr) + ")";
                    lit_tab[lit_tab_ptr++] = make_pair(literal_val, -1);
                } else {
                    int symbol_index = update_symbol(operand2, -1);
                    ic_line += "(" + to_string(register_codes[operand1]) + ") (S," + to_string(symbol_index) + ")";
                }
            }
            location_cntr += 1;
        }

        ic_lines.push_back(ic_line);
    }

    init_literals();

    cout << "-------------- INTERMEDIATE CODE----------------" << endl;
    for (const auto& line : ic_lines) {
        cout << line << endl;
    }

    cout << "--------- SYMBOL TABLE -------------" << endl;
    for (const auto& entry : symtab) {
        cout << entry.first << " " << entry.second << endl;
    }

    cout << "--------- LITERAL TABLE -------------" << endl;
    for (int i = 0; i < lit_tab_ptr; ++i) {
        cout << lit_tab[i].first << " " << lit_tab[i].second << endl;
    }

    cout << "---------- POOL TABLE -------------" << endl;
    for (int i = 0; i < pool_tab_ptr; ++i) {
        cout << pool_tab[i] << endl;
    }

    return 0;
}