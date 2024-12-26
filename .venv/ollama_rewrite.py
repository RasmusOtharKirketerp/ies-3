# prompt.py
import ollama
# Define the model and the message
model_name = 'mistral'  # Replace with your desired model

def generate_summary_prompt(article_text):
    """
    Generates a prompt for an LLM to summarize an article and remove clickbait language.
    
    Parameters:
    - article_text (str): The text of the article to summarize.
    
    Returns:
    - str: The generated prompt with the article text embedded.
    """
    
    # Define the prompt template
    prompt_template = """
    You are an expert summarizer and content refiner. Given an article, your task is to provide a concise summary that captures the main ideas, removes unnecessary embellishments, and avoids clickbait language.

    ### Steps:
    1. Read and understand the article’s main points.
    2. Identify any clickbait or exaggerated phrases (e.g., "You won't believe," "shocking," "top secrets revealed") and remove or replace them with straightforward language.
    3. identify the language the aricle is written in and maintain this lauguage in reply.



    ### Article Text:
    {article}

    ### Expected Output:
    - Reply in Danish
    - Five key words.
    - A short resume in two lines.
    - The rewritten article as a concise, neutral summary with no clickbait language.
    - Key points presented clearly, without unnecessary details or hype.

    Provide the refined summary. Just the facts, no fluff, and don't tell what you changed.
    """
    
    # Insert the article text into the prompt template
    prompt_with_article = prompt_template.format(article=article_text)
    
    return prompt_with_article

def rewrite_text(str):
    str = generate_summary_prompt(str)
    messages = [{'role': 'user', 'content': str}]
    response = ollama.chat(model=model_name, messages=messages)
    return response['message']['content']

# Example usage
if __name__ == "__main__":
    sample_article = """"Årets afsmeltning af norske gletsjere beskrives af en forsker som ""chokerende"".

I årtier har der været tilbagegang i de norske gletsjere.

Men sommerens afsmeltning af særligt to gletsjere i Nordnorge får en forsker til at udtrykke bekymring. De har mistet fire gange så meget tykkelse som normalt.

- Årets tal var helt specielle, lidt chokerende for mig som gletsjerforsker at se så stor afsmeltning på et år, siger Liss Marie Andreassen fra Norges direktorat for vandressourcer og energi (NVE) ifølge NTB.

Der er tale om gletsjerne Langfjordjøkulen i Finnmark og Engagletsjeren i Nordland, som hver har mistet fire meter i tykkelse.

Langfjordjøkulen er omkring 50 meter tyk. Dermed er den blevet cirka ti procent tyndere på et år. Det skriver det norske public service-medie NRK.

- Vi har aldrig målt den slags tal før på disse gletsjere. Og det var slet og ret en ekstraordinær afsmeltning i år, selv om vi vidste, sommeren var meget varm, siger Andreassen til mediet.

Lyn-analyse Man bliver ikke længere overrasket, når man læser om de norske gletsjere. Det er forventeligt, at når klimaet på kloden fortsætter sin uophørlige stigning mod nye temperaturrekorder, så smelter isen. Det, man må frygte, er, at den accelererede afsmeltning er et tegn på, at vi nærmer os et tipping point – et punkt, hvor udviklingen går så hurtigt, at der ikke længere er nogen vej tilbage. Allerede for næsten ti år siden advarede forskere om, at alle gletsjere i Norge kunne være forsvundet ved udgangen af dette århundrede. Nu frygter man, at det kan ske endnu hurtigere. Endnu en gang løfter naturen det røde flag og advarer os om konsekvenserne af den globale opvarmning. Alligevel endte politikerne på det seneste klimatopmøde med at bukke under for spil om magt og penge frem for at finde reelle løsninger.

34 ud af 35 gletsjere har trukket sig tilbage

I alt har NVE målt gletsjerfronterne 35 steder i landet, og alle bortset fra én gletsjer har trukket sig tilbage, skriver NTB.

Nigardgletsjeren ligger i Vestland i det sydlige Norge og er et populært turistmål. Den har trukket sig så meget tilbage, at den ikke længere er synlig fra et af de sædvanlige fotosteder.

Derfor må turister nu gå længere hen mod gletsjeren for at tage billeder.

- Gletsjerne smelter på grund af klimaforandringerne. De er meget følsomme over for klimaforandringer og justerer deres størrelse ved at vokse eller skrumpe, når klimaet ændrer sig, siger Andreassen.

Gletsjerne står til at forsvinde

Ifølge et studie fra 2023 står halvdelen af Jordens gletsjere – især de mindre – til at forsvinde inden slutningen af århundredet på grund af klimaforandringer.

De første er dog allerede forsvundet.

Tilbage i foråret stod det klar, at Humboldt-gletsjeren i Venezuela var skrumpet så meget, at forskere degraderede den til blot at være en isflade på et par hektar.

Dermed er Venezuela og Slovenien de to første lande, der har mistet deres gletsjere i moderne tid.

Indonesiens Puncak Jaya, ironisk nok også kendt som “Evighedsgletsjeren,” vil sandsynligvis følge trop inden for de næste to år som Asiens sidste tropiske gletsjer.

Også de europæiske gletsjere er i fare for at forsvinde.

Mindst 30 procent af Alpernes gletsjere risikerer at være væk i 2050 – selv uden yderligere opvarmning.

Fortsætter CO₂-udledningen på det nuværende niveau, er der 60 til 70 procent risiko for, at gletsjerne vil være smeltet bort i 2050."""
    prompt = generate_summary_prompt(sample_article)
    #print(prompt)
    print(rewrite_text(sample_article))
