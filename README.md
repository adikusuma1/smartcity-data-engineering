# Smart City Streaming Data Pipeline 🚦🏙️

Proyek ini merupakan bagian dari portofolio data engineering yang dirancang untuk menyimulasikan dan memproses data streaming dalam konteks **Smart City** menggunakan Apache Kafka dan Apache Spark.

## 🧠 Deskripsi Proyek

Proyek ini menyimulasikan arus data dari berbagai sensor kota pintar (GPS kendaraan, kamera lalu lintas, cuaca, dan insiden darurat) dan memprosesnya secara real-time menggunakan Spark Structured Streaming. Data dikirim melalui Kafka, lalu disimpan dalam format Parquet ke AWS S3.

### Komponen Utama:
- **Data Simulation**: Generator data Python yang menghasilkan data kendaraan, GPS, cuaca, kamera lalu lintas, dan insiden.
- **Kafka Cluster**: Infrastruktur berbasis Docker menggunakan Kafka, Zookeeper, dan broker.
- **Spark Streaming**: Spark membaca data real-time dari Kafka, melakukan parsing schema, dan menyimpannya ke AWS S3.
- **Docker Compose**: Mengorkestrasi seluruh layanan secara terintegrasi.

---

## 🗂️ Struktur Proyek

```bash
.
├── data_engineering/
│   ├── jobs/
│   │   ├── main.py              # Generator data streaming
│   │   ├── config.py            # Konfigurasi environment AWS
│   │   └── spark-city.py        # Pipeline streaming Spark
│   └── docker-compose.yml       # Orkestrasi Kafka, Spark, dll.
├── DE_SCity/
│   └── jobs/
│       └── try.py               # Eksperimen lain
├── image/                       # Folder gambar/visualisasi (jika ada)
├── requirements.txt             # Dependencies Python
└── README.md
```

##⚙️ Teknologi yang Digunakan
- **Komponen  Teknologi
- Data Generator  Python + Confluent Kafka
- Messaging	Apache Kafka + Zookeeper (via Docker)
- Stream Process	Apache Spark Structured Streaming (3.5.0)
- Penyimpanan	AWS S3 (via Hadoop AWS Connector)
- Orkestrasi	Docker Compose
