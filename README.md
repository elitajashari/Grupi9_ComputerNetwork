# Grupi9_ComputerNetwork
# UDP File Management & Monitoring System

Ky projekt implementon një sistem komunikimi Client-Server bazuar në protokollin UDP, i shoqëruar me një ndërfaqe monitorimi përmes protokollit HTTP. Sistemi lejon menaxhimin e skedarëve në distancë dhe kontrollin e qasjes në kohë reale.

---

##  Si funksionon sistemi

Sistemi operon përmes dy skedarëve kryesorë që bashkëveprojnë me njëri-tjetrin:

### 1. Serveri (`server.py`)
Serveri është "truri" i sistemit dhe kryen dy detyra paralele:
* **Komunikimi UDP (Porti 9999):** Serveri dëgjon për kërkesa nga klientët. Ai përpunon komandat për leximin, listimin dhe fshirjen e skedarëve. Për çdo kërkesë, serveri verifikon IP-në e dërguesit për të përcaktuar nëse ka privilegje administratori (për komandat si `/delete`).
* **Monitorimi HTTP (Porti 8080):** Serveri mbledh statistika për çdo mesazh të pranuar dhe i shfaq ato në një format JSON që mund të aksesohet përmes çdo browser-i.

### 2. Klienti (`client_udp.py`)
Klienti shërben si ndërfaqja e përdoruesit për të ndërvepruar me serverin:
* Përdoruesi shkruan komandën në terminal.
* Klienti validon formatin e komandës dhe ia dërgon serverit përmes paketave UDP.
* **Timeout Mechanism:** Klienti është i programuar që nëse serveri nuk përgjigjet brenda 3 sekondave, të ndërpresë pritjen dhe të njoftojë përdoruesin për mungesë lidhjeje.

---



## 🚀 Udhëzimet për Ekzekutim

Për ta vënë projektin në punë, ndiqni këto hapa:

1.  **Nisni Serverin:**
    Hapni terminalin dhe ekzekutoni skedarin kryesor të serverit:
    ```bash
    python server.py
    ```
    *Serveri tani është aktiv dhe pret kërkesa në portin 9999.*

2.  **Nisni Klientin:**
    Në një dritare të re terminali, ekzekutoni skedarin e klientit:
    ```bash
    python client_udp.py
    ```

3.  **Monitorimi në Browser:**
    Për të parë statistikat e sistemit (mesazhet totale, përdoruesit aktivë, log-et), hapni browser-in dhe shkruani:
    `http://10.180.23.44:8080/stats`

---

## 📋 Komandat e mbështetura

| Komanda | Funksioni |
| :--- | :--- |
| `/list` | Liston të gjithë skedarët që ndodhen në folderin e serverit. |
| `/read [emri_file]` | Shfaq përmbajtjen tekstuale të një skedari të caktuar. |
| `/info [emri_file]` | Kthen detaje si madhësia (bytes) dhe data e krijimit të skedarit. |
| `/delete [emri_file]` | Fshin skedarin (kërkon që IP-ja e përdoruesit të jetë në listën e Admin). |
| `/upload [emri_file]` | Simulon procesin e ngarkimit të një skedari në server. |
| `exit` | Mbyll lidhjen e klientit dhe ndalon programin. |

---
*Ky projekt është zhvilluar si pjesë e lëndës "Rrjeta Kompjuterike".*
