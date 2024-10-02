#include <iostream>
#include <string>
#include <cpr/cpr.h>


class Ville {
private:
    std::string nom;
    std::string code_postal;
    double prix_m2;

public:
    // Constructeur par défaut
    Ville() : nom(""), code_postal(""), prix_m2(0.0) {}

    // Constructeur avec paramètres
    Ville(std::string n, std::string cp, double prix) : nom(n), code_postal(cp), prix_m2(prix) {}



    // Méthode pour afficher les détails de la ville
    void afficher() const {
        std::cout << "Ville: " << nom << ", Code Postal: " << code_postal << ", Prix au m2: " << prix_m2 << std::endl;
    }
};

int main() {

    Ville v("Toulouse", "31100", 3000.0);

    // Appeler la méthode afficher() pour imprimer les détails de l'instance
    v.afficher();

    return 0; // Retourner 0 pour indiquer que le programme s'est bien terminé
}
