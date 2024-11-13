#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <utility>

using namespace std;

int main() {
    string ic_file_path;
    cout << "Enter IC file path: ";
    getline(cin, ic_file_path);

    ifstream ic_file(ic_file_path);
    vector<vector<string>> ic_line_tokens;
    if (ic_file.is_open()) {
        string line;
        while (getline(ic_file, line)) {
            istringstream iss(line);
            vector<string> tokens;
            string token;
            while (iss >> token) {
                tokens.push_back(token);
            }
            ic_line_tokens.push_back(tokens);
        }
        ic_file.close();
    } else {
        cerr << "Error opening IC file." << endl;
        return 1;
    }

    vector<pair<string, int>> sym_tab;
    string sym_tab_filepath;
    cout << "Enter symbol table filepath: ";
    getline(cin, sym_tab_filepath);

    ifstream sym_tab_file(sym_tab_filepath);
    if (sym_tab_file.is_open()) {
        string line;
        while (getline(sym_tab_file, line)) {
            istringstream iss(line);
            string name;
            int addr;
            iss >> name >> addr;
            sym_tab.emplace_back(name, addr);
        }
        sym_tab_file.close();
    } else {
        cerr << "Error opening symbol table file." << endl;
        return 1;
    }

    vector<pair<string, int>> lit_tab;
    string lit_tab_filepath;
    cout << "Enter literal table filepath: ";
    getline(cin, lit_tab_filepath);

    if (!lit_tab_filepath.empty()) {
        ifstream lit_tab_file(lit_tab_filepath);
        if (lit_tab_file.is_open()) {
            string line;
            while (getline(lit_tab_file, line)) {
                istringstream iss(line);
                string name;
                int addr;
                iss >> name >> addr;
                lit_tab.emplace_back(name, addr);
            }
            lit_tab_file.close();
        } else {
            cerr << "Error opening literal table file." << endl;
            return 1;
        }
    }

    for (const auto& line_tokens : ic_line_tokens) {
        if (line_tokens.size() == 4) {
            string lc = line_tokens[0];
            string mnemonic_opcode = line_tokens[1].substr(1, line_tokens[1].find(',') - 1);

            vector<string> operand1_tokens;
            istringstream iss1(line_tokens[2].substr(1, line_tokens[2].size() - 2));
            string part;
            while (getline(iss1, part, ',')) {
                operand1_tokens.push_back(part);
            }

            string operand1 = "";
            if (operand1_tokens.size() == 2 && operand1_tokens[0] == "S") {
                int sym_tab_index = stoi(operand1_tokens[1]);
                operand1 = to_string(sym_tab[sym_tab_index].second);
            } else {
                operand1 = operand1_tokens[0];
            }

            vector<string> operand2_tokens;
            istringstream iss2(line_tokens[3].substr(1, line_tokens[3].size() - 2));
            while (getline(iss2, part, ',')) {
                operand2_tokens.push_back(part);
            }

            string operand2 = "";
            if (operand2_tokens[0] == "S") {
                int sym_tab_index = stoi(operand2_tokens[1]);
                operand2 = to_string(sym_tab[sym_tab_index].second);
            } else if (operand2_tokens[0] == "L") {
                int lit_tab_index = stoi(operand2_tokens[1]);
                operand2 = to_string(lit_tab[lit_tab_index].second);
            } else if (operand2_tokens[0] == "C") {
                operand2 = operand2_tokens[1];
                if (operand2.find('\'') != string::npos) {
                    operand2 = operand2.substr(1, operand2.size() - 2);
                }
            }

            cout << lc << " " << mnemonic_opcode << " " << operand1 << " " << operand2 << endl;

        } else if (line_tokens.size() == 2) {
            if (isdigit(line_tokens[0][0])) {
                string lc = line_tokens[0];
                string mnemonic_opcode = line_tokens[1].substr(1, line_tokens[1].find(',') - 1);
                cout << lc << " " << mnemonic_opcode << endl;
            } else {
                string mnemonic_opcode = line_tokens[0].substr(1, line_tokens[0].find(',') - 1);
                vector<string> operand1_tokens;
                istringstream iss1(line_tokens[1].substr(1, line_tokens[1].size() - 2));
                string part;
                while (getline(iss1, part, ',')) {
                    operand1_tokens.push_back(part);
                }

                string operand1 = "";
                if (operand1_tokens.size() == 2 && operand1_tokens[0] == "S") {
                    int sym_tab_index = stoi(operand1_tokens[1]);
                    operand1 = to_string(sym_tab[sym_tab_index].second);
                } else {
                    operand1 = operand1_tokens[0];
                }

                cout << mnemonic_opcode << " " << operand1 << endl;
            }
        }
    }

    return 0;
}