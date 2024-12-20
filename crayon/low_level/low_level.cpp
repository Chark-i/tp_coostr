#include <iostream>
#include <string>
#include <cpr/cpr.h>
#include <fstream>
#include <nlohmann/json.hpp>
#include <memory>

using json = nlohmann::json_abi_v3_11_3::json;



class Ville {
private:
    int id;
    std::string nom;
    double code_postal;
    double prix_m2;

public:
  //  Ville() : nom(""), code_postal(00000), prix_m2(0.0) {}

  //  Ville(std::string n, std::string cp, double prix) : nom(n), code_postal(cp), prix_m2(prix) {}

  //  Ville(std::string n, std::string cp, double prix) : nom(n), code_postal(n), prix_m2(n) {}

  //  Ville (json q) : nom(q["nom"]), code_postal(q["code_postal"]), prix_m2(q["prix_m2"]) {};

    Ville(int id_des) : id(0),  nom(""), code_postal(00000), prix_m2(0.0) {
      cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/ville/"+ std::to_string(id_des)});

      r.status_code;

      if (r.status_code != 200) {
        std::cout<<"erreur dans l'ouverture du lien http"<<std::endl;
        return;
      }

      r.header["content-type"];
      r.text;
    //  std::cout<<r.text<<std::endl;
      json data = json::parse(r.text);

      id = id_des;
      nom = data["nom"];
      code_postal = data["code_postal"].get<double>();
      prix_m2 = data["prix_m2"].get<double>();
    }

   void afficher() const {
        std::cout << "Ville: " << nom << ", Code Postal: " << code_postal << ", Prix au m2: " << prix_m2 << std::endl;
    }
    };

class Machine {
private:
  int id;
  std::string nom;
  double prix;
  double n_serie;

public:

    Machine(int id_des)  {
      cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/machine/"+ std::to_string(id_des)});

      r.status_code;

      if (r.status_code != 200) {
        std::cout<<"erreur ici"<<std::endl;
        std::cout<<"erreur dans l'ouverture du lien http"<<std::endl;
        return;
      }

      r.header["content-type"];
      r.text;

    //  std::cout<<r.text<<std::endl;

      json data = json::parse(r.text);
      id = id_des;
      nom = data["nom"];
      prix = data["prix"].get<double>();
      n_serie = data["n_serie"].get<double>();

  }

  void afficher() const {
      std::cout << "Nom: " << nom << ", prix: " << prix << ", n_serie: " << n_serie << std::endl;
  }
  };

class Local{
protected:
  std::string nom;
  std::string ville;
  double surface;

public:
  Local(std::string n, std::string v, double s) : nom(n), ville(v), surface(s) {}
  virtual void afficher() const = 0;

};

class Siege_social:public Local{
public:
  Siege_social(int id) : Local("","",0){

    cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/siege_social/"+ std::to_string(id)});

    r.status_code;

    if (r.status_code != 200) {
      std::cout<<"erreur dans l'ouverture du lien http"<<std::endl;
      return;
    }

    r.header["content-type"];
    r.text;

    json data = json::parse(r.text);
    std::cout<<r.text<<std::endl;

    nom = data["nom"];
    ville = data["ville"];
    surface = data["surface"].get<double>();

  }

  void afficher() const {
      std::cout << "Nom: " << nom << ", ville: " << ville << ", surface: " << surface << std::endl;
  }


};

class Usine:public Local{
private:
      std::vector<std::unique_ptr<Machine>> machines;
      std::unique_ptr<Ville> ville;
      double surface;
public:
    Usine(int id) : Local("", "", 0), ville(nullptr),surface(0) {

    cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/usine/"+ std::to_string(id)});

    r.status_code;

    if (r.status_code != 200) {
      std::cout<<"erreur dans l'ouverture du lien http"<<std::endl;
      return;
    }

    r.header["content-type"];
    r.text;
  //  std::cout<<r.text<<std::endl;
    json data = json::parse(r.text);


    nom = data["nom_usine"];
    surface = data["surface"].get<double>();
    ville = std::make_unique<Ville>(data["ville"]["id"]);


    for (const auto& machine_data : data["machines"]) {
    int machine_id = machine_data["id"].get<int>();
    machines.push_back(std::make_unique<Machine>(machine_id));
}

  }

  void afficher() const override {
        std::cout << "Usine: Nom: " << nom << ", Surface: " << surface <<", ";
        if (ville) ville->afficher();
        std::cout << "Machines de cette Usine:"<<std::endl;
        for (const auto& machine : machines) {
            machine->afficher();
        }
    }
};

class Objet{
protected:
  std::string nom;
  double prix;

public:
  Objet(std::string n, double p) : nom(n), prix(p) {}
  virtual void afficher() const = 0;

};

class Ressource : public Objet {
public:
    // Constructeur
    Ressource(const std::string n, double p) : Objet(n, p) {}

    // Implémentation de la méthode afficher
    void afficher() const override {
        std::cout << "Ressource: " << nom
                  << ", Prix: " << prix << "€"
                  << std::endl;
    }
};

class Quantite_Ressource {
private:
    std::unique_ptr<Ressource> ressource;
    int quantite;

public:
    // Constructeur
    Quantite_Ressource(std::unique_ptr<Ressource> r, int q)
        : ressource(std::move(r)), quantite(q) {}

    void afficher() const {
        std::cout << "Quantité de ";
        ressource->afficher();
        std::cout << "Quantité: " << quantite << std::endl;
    }
};




int main() {



  //Ville v("Toulouse", 31100, 3000.0);



  /*
    cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/ville/1"});

    r.status_code;

    if (r.status_code != 200) {
      std::cout<<"erreur dans l'ouverture du lien http"<<std::endl;
    }

    r.header["content-type"];
    r.text;


    std::cout << r.text << std::endl;

    json data = json::parse(r.text);
    */

    //Ville v(1);

    //v.afficher();
//
    //Machine m(1);

    //m.afficher();

    Usine U(1);
    U.afficher();

    //std::cout << data << std::endl;

    return 0;
}
