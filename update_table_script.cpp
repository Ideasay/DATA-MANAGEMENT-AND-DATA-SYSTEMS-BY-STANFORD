#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    
    while(getline(cin, s)) {
        cout << "UPDATE `third-diorama-233818.1.survey_results_public_sample`\n";
        cout << "SET " << s << " = NULL\n";
        cout << "WHERE " << s << " LIKE 'NA'\n";
        
        cout << '\n';
    }
}
