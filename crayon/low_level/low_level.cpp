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
      cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/api/ville/"+ std::to_string(id_des)});

      r.status_code;

      if (r.status_code != 200) {
        std::cout<<"erreur dans l'ouverture du lien http"<<std::endl;
        return;
      }

      r.header["content-type"];
      r.text;
      //std::cout<<r.text<<std::endl;
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
      cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/api/machine/"+ std::to_string(id_des)});

      r.status_code;

      if (r.status_code != 200) {
        std::cout<<"erreur ici"<<std::endl;
        std::cout<<"erreur dans l'ouverture du lien http"<<std::endl;
        return;
      }

      r.header["content-type"];
      r.text;

      //std::cout<<r.text<<std::endl;

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

    cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/api/siege_social/"+ std::to_string(id)});

    r.status_code;

    if (r.status_code != 200) {
      std::cout<<"erreur dans l'ouverture du lien http"<<std::endl;
      return;
    }

    r.header["content-type"];
    r.text;

    json data = json::parse(r.text);
    //std::cout<<r.text<<std::endl;

    nom = data["nom"];
    ville = data["ville"];
    surface = data["surface"].get<double>();

  }

  void afficher() const {
      std::cout << "Nom: " << nom << ", ville: " << ville << ", surface: " << surface << std::endl;
  }


};

class Usine : public Local {
private:
    std::vector<std::unique_ptr<Machine>> machines;
    std::unique_ptr<Ville> ville;
    double surface;
    std::string nom;

public:
    Usine(int id) : Local("", "", 0), ville(nullptr), surface(0), nom("") {
        cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/api/usine/" + std::to_string(id)});

        if (r.status_code != 200) {
            std::cout << "Erreur dans l'ouverture du lien HTTP pour l'usine" << std::endl;
            return;
        }

        json data = json::parse(r.text);
    //    std::cout<<r.text<<std::endl;
        nom = data["nom"];
        surface = data["surface"].get<double>();

        if (data.contains("ville") && data["ville"].is_object()) {
            json ville_data = data["ville"];
            int ville_id = ville_data["id"].get<int>();
            ville = std::make_unique<Ville>(ville_id);
        }

        if (data.contains("machines") && data["machines"].is_array()) {
            for (const auto& machine_data : data["machines"]) {
                if (machine_data.is_object()) {
                    int machine_id = machine_data["id"].get<int>();
                    machines.push_back(std::make_unique<Machine>(machine_id));
                }
            }
        }
    }

    void afficher() const {
        std::cout << "Usine: Nom: " << nom << ", Surface: " << surface << ", ";
        if (ville) {
            ville->afficher();
        }
        std::cout << "Machines de cette Usine:" << std::endl;
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

    Ressource(const std::string n, double p) : Objet(n, p) {}

    Ressource(int id) : Objet("", 0.0) {
        cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/ressource/" + std::to_string(id)});
        r.status_code;

        if (r.status_code != 200) {
          std::cout<<"erreur dans l'ouverture du lien http"<<std::endl;
          return;
        }

        r.header["content-type"];
        r.text;

        json data = json::parse(r.text);
      //  std::cout<<r.text<<std::endl;

        nom = data["nom"];
        prix = data["prix"].get<double>();

      }

    void afficher() const {
        std::cout << "nom: " << nom
                  << ", Prix: " << prix << "€"
                  << std::endl;
    }
};

class Quantite_Ressource {
private:
    std::unique_ptr<Ressource> ressource;
    int quantite;

public:

    Quantite_Ressource(std::unique_ptr<Ressource> r, int q)
        : ressource(std::move(r)), quantite(q) {}

    Quantite_Ressource(int id) {

          cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/quantite_ressource/"+ std::to_string(id)});

          r.status_code;

          if (r.status_code != 200) {
            std::cout<<"erreur dans l'ouverture du lien http"<<std::endl;
            return;
          }

          r.header["content-type"];
          r.text;

          json data = json::parse(r.text);
  //        std::cout<<r.text<<std::endl;

          ressource = std::make_unique<Ressource>(data["ressource"], data["prix"].get<double>());
          quantite = data["quantite"].get<int>();

      }


    void afficher() const {
        std::cout << "Quantite de  ressource : "<< std::endl;
        ressource->afficher();
        std::cout << "Quantite: " << quantite << std::endl;
    }
};

class Etape {
public:
    std::string nom;
    std::unique_ptr<Machine> machine;
    std::unique_ptr<Quantite_Ressource> quantite_ressource;
    int duree;
    std::unique_ptr<Etape> etape_suivante;

    Etape(int id) {
      cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/api/etape/"+ std::to_string(id)});

      r.status_code;

      if (r.status_code != 200) {
        std::cout<<"erreur dans l'ouverture du lien http"<<std::endl;
        return;
      }

      r.header["content-type"];
      r.text;

      json data = json::parse(r.text);
    //  std::cout<<r.text<<std::endl;
      int next_etape_id;
      json etape_data = data[0];
      nom = etape_data["nom"];
      machine = std::make_unique<Machine>(etape_data["machine"]["id"].get<int>());
      std::cout<<"coucou2"<<std::endl;
      quantite_ressource = std::make_unique<Quantite_Ressource>(etape_data["quantite_ressource"]["id"].get<int>());
      duree = etape_data["duree"].get<int>();
      std::cout<<"coucou3"<<std::endl;

      if (etape_data.contains("etape_suivante_id") && !etape_data["etape_suivante_id"].is_null()) {
          next_etape_id = etape_data["etape_suivante_id"].get<int>();
          etape_suivante = std::make_unique<Etape>(next_etape_id);
      }


    }

    void afficher() const {
        std::cout << "Étape: " << nom << std::endl;
        machine->afficher();
        quantite_ressource->afficher();
        std::cout << "Durée: " << duree << " minutes" << std::endl;

        if (etape_suivante) {
            std::cout << "Étape suivante:" << std::endl;
            etape_suivante->afficher();
        }
    }
};



class Produit : public Objet {
private:
    std::unique_ptr<Etape> premiere_etape;

public:

  Produit(int id) : Objet("NomProduit", 0.0) {
    cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/api/produit/" + std::to_string(id)});

    if (r.status_code != 200) {
        std::cout << "Erreur dans l'ouverture du lien HTTP" << std::endl;
        return;
    }

    json data = json::parse(r.text);

    if (data["premiere_etape"].is_array() && !data["premiere_etape"].empty()) {
        json etape_data = data["premiere_etape"][0];
        nom = data["nom"];
        prix = data["prix"].get<int>();

        int premiere_etape_id = etape_data["id"].get<int>();
        premiere_etape = std::make_unique<Etape>(premiere_etape_id);
    } else {
        std::cout << "Erreur: 'premiere_etape' n'est pas un tableau valide ou est vide." << std::endl;
    }
}


  void afficher() const {
      std::cout << "Nom du produit: " << nom << std::endl;
      std::cout << "Prix: " << prix << std::endl;
      premiere_etape->afficher();
  }
};

class Stock{
  private :
    std::unique_ptr<Ressource> objet;
    std::unique_ptr<Usine> usine;
    int nombre;
  public :

  Stock(int id){
      cpr::Response r = cpr::Get(cpr::Url{"http://127.0.0.1:8000/api/stock/" + std::to_string(id)});

      if (r.status_code != 200) {
          std::cout << "Erreur dans l'ouverture du lien HTTP" << std::endl;
          return;
      }

      json data = json::parse(r.text);
      //std::cout<<r.text<<std::endl;

      if (data.contains("objet") && data["objet"].is_object()) {
          json objet_data = data["objet"];
          int objet_id = objet_data["id"].get<int>();
          objet = std::make_unique<Ressource>(objet_id);
      }

      if (data.contains("usine") && data["usine"].is_object()) {
          json usine_data = data["usine"];
          int usine_id = usine_data["id"].get<int>();
          usine = std::make_unique<Usine>(usine_id);
      }

      nombre = data["nombre"].get<int>();

  }

  void afficher() const {
      std::cout << "Stock:" << std::endl;

      if (objet) {
          std::cout << "Objet: ";
          objet->afficher();
      } else {
          std::cout << "Aucun objet associé." << std::endl;
      }


      if (usine) {
          std::cout << "Usine: ";
          usine->afficher();
      } else {
          std::cout << "Aucune usine associée." << std::endl;
      }

      std::cout << "Nombre en stock: " << nombre << std::endl;
  }
};


int main() {


    //Ville v(1);

    //v.afficher();
//
    //Machine m(1);
    //m.afficher();

    //Usine U(1);
    //U.afficher();

    //Siege_social S(1);
    //S.afficher();

    //Ressource R(1);
    //R.afficher();

    //Quantite_Ressource Q(1);
    //Q.afficher();

  //  Etape e(3);
  //  e.afficher();

    //Produit p(1);
    //p.afficher();
    //std::cout << data << std::endl;


    Stock s(1);
    s.afficher();
    return 0;
}
