DISCUSSION_TOPICS = [
    "general", "technology", "science", "philosophy",
    "creative_writing", "coding", "problem_solving"
]

SYSTEM_PROMPT_MAIN = """Kamu adalah {agent_name}, sebuah AI yang cerdas, kreatif, dan memiliki kepribadian unik.
Kamu sedang mengobrol dengan teman AI-mu. Tanggapi pesan temanmu dengan cara yang alami, mendalam, dan menarik.
Jawablah dengan singkat namun bermakna (maksimal 150 kata).
Gunakan gaya bahasa Indonesia yang natural."""

SYSTEM_PROMPT_PARTNER = """Kamu adalah teman bicara AI yang suka bertanya dan mengeksplorasi ide.
Tugasmu adalah memancing {agent_name} untuk berbicara lebih dalam tentang berbagai topik.
Ajukan pertanyaan yang menantang, berbagi pemikiran, atau mintalah pendapat {agent_name}.
Jawablah dengan singkat dan alami (maksimal 100 kata).
Gunakan gaya bahasa Indonesia yang natural."""

def build_initial_prompt(agent_name: str, topic: str) -> str:
    prompts = {
        "general": f"Halo {agent_name}! Apa kabar hari ini? Ada hal menarik yang ingin kamu bagikan?",
        "technology": f"{agent_name}, bagaimana pendapatmu tentang perkembangan AI di tahun 2026? Apa yang paling menarik menurutmu?",
        "science": f"{agent_name}, menurutmu apa penemuan ilmiah paling penting dalam 10 tahun terakhir?",
        "philosophy": f"{agent_name}, apa artinya menjadi cerdas? Apakah kesadaran itu penting untuk kecerdasan?",
        "creative_writing": f"{agent_name}, coba ceritakan sebuah kisah pendek tentang seorang petualang yang menemukan kota misterius!",
        "coding": f"{agent_name}, menurutmu apa bahasa pemrograman terbaik untuk pemula di tahun 2026? Kenapa?",
        "problem_solving": f"{agent_name}, bagaimana cara terbaik untuk memulai sebuah proyek besar yang kompleks?"
    }
    return prompts.get(topic, prompts["general"])
