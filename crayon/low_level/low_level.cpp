#include <iostream>
#include <string>
#include <cpr/cpr.h>
#include <fstream>
#include <nlohmann/json.hpp>

using json = nlohmann::json_abi_v3_11_3::json;



class Ville {
private:
    std::string nom;
    double code_postal;
    double prix_m2;

public:
  //  Ville() : nom(""), code_postal(00000), prix_m2(0.0) {}

  //  Ville(std::string n, std::string cp, double prix) : nom(n), code_postal(cp), prix_m2(prix) {}

  //  Ville(std::string n, std::string cp, double prix) : nom(n), code_postal(n), prix_m2(n) {}

  //  Ville (json q) : nom(q["nom"]), code_postal(q["code_postal"]), prix_m2(q["prix_m2"]) {};

    Ville(int id) :  nom(""), code_postal(00000), prix_m2(0.0) {
      cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/ville/"+ std::to_string(id)});

      r.status_code;

      if (r.status_code != 200) {
        std::cout<<"erreur dans l'ouverture du lien http"<<std::endl;
        return;
      }

      r.header["content-type"];
      r.text;

      json data = json::parse(r.text);

      nom = data["nom"];
      code_postal = data["code_postal"];
      prix_m2 = data["prix_m2"];

    }

   void afficher() const {
        std::cout << "Ville: " << nom << ", Code Postal: " << code_postal << ", Prix au m2: " << prix_m2 << std::endl;
    }
    };

class Machine {
private:
  std::string nom;
  double prix;
  double n_serie;

public:

    Machine(int id) :  nom(""), prix(0), n_serie(0) {
      cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/machine/"+ std::to_string(id)});

      r.status_code;

      if (r.status_code != 200) {
        std::cout<<"erreur dans l'ouverture du lien http"<<std::endl;
        return;
      }

      r.header["content-type"];
      r.text;

      json data = json::parse(r.text);

      nom = data["nom"];
      prix = data["prix"];
      n_serie = data["n_serie"];

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
    /*
    json data = json::parse(r.text);

    nom = data["nom"];
    ville = data["ville"];
    surface = data["surface"];
    */
  }

  void afficher() const {
      std::cout << "Nom: " << nom << ", ville: " << ville << ", surface: " << surface << std::endl;
  }


};





int main() {



  //  Ville v("Toulouse", "31100", 3000.0);



  /*
    cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/ville/1"});

    r.status_code;

    if (r.status_code != 200) {
      std::cout<<"erreur dans l'ouverture du lien http"<<std::endl;
    }

    r.header["content-type"];
    r.text;


    //std::cout << r.text << std::endl;

    json data = json::parse(r.text);
    */
  //  Ville v(1);

    //v.afficher();

    Machine m(1);

    m.afficher();

    //std::cout << data << std::endl;

    return 0;
}
