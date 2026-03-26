from app.config.sbert_config import sbert_model
from app.schemas.ticket_trans_schema import TicketAgenticChatSch
from sentence_transformers import util

def ticket_field_validator(state:TicketAgenticChatSch):
    #mock data
    datas = [
        {
            "project_code":"PIK2",
            "project_name":"Pantai Indah Kapuk 2",
            "project_description":"Kawasan Pantai Indah Kapuk 2 terbaru yang mencakup area perumahan"
        },
        {
            "project_code":"ALH",
            "project_name":"ALOHA",
            "project_description":"Kawasan wisata pantai pasir putih dengan tenant tenant menarik"
        },
        {
            "project_code":"OSA",
            "project_name":"OSAKA",
            "project_description":"Hotel dan apartement bernuansa jepang"
        },
        {
            "project_code":"SAN",
            "project_name":"SAN ANTONIO",
            "project_description":"Hotel dan apartement bernuansa jepang"
        },
    ]

    #count cosine similarity (min threshold 0.7) --> ngecek akurasi data
    threshold = 0.5
    similarity = []
    validation_description:str=''
    for data in datas:
        similarity.append(util.cos_sim
            (sbert_model.encode(state.ticket_schema.project_code),
            sbert_model.encode(str(data['project_code']))))
        
    similarity_max = max(similarity)

    if(similarity_max >= threshold):
            validation_description=f'Apakah yang kamu maksud adalah project {datas[similarity.index(similarity_max)]['project_name']}?'
        
    return{
        'long_answer':f'{state.long_answer}\n{validation_description}',
    }
    
