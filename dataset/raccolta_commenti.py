import praw
import pandas as pd
from datetime import datetime
import time

# Configurazione Reddit API
CLIENT_ID = "INSERIRE_API_KEY"  
CLIENT_SECRET = "INSERIRE_API_KEY"  
# ========================================


try:
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent="sentiment_analysis_gaza"
    )
    
    # Test della connessione
    print("Test connessione a Reddit API...")
    user = reddit.user.me()
    print(f"Connesso come: {user}\n")

except Exception as e:
    print(f" Errore di autenticazione: {e}")
    exit()

# Keyword per la ricerca iniziale dei post

keywords_by_country = {
    "france": ["gaza", "palestine", "israel", "israël", "hamas"],
    "de": ["gaza", "palästina", "israel", "hamas"],
    "italy": ["gaza", "palestina", "israele", "hamas"],
    "unitedkingdom": ["gaza", "palestine", "israel", "hamas"],
    "spain": ["gaza", "palestina", "israel", "hamas"],
    "poland": ["gaza", "palestyna", "izrael", "israel", "hamas"],
    "netherlands": ["gaza", "palestina", "israël", "hamas"],  
    "sweden": ["gaza", "palestina", "israel", "hamas"], 
    "norway": ["gaza", "palestina", "israel", "hamas"],  
    "denmark": ["gaza", "palestina", "israel", "hamas"], 
    "ukraine":["gaza", "газа", "палести́на", "israel", "ізраїль", "хамас"],
    "portugal": ["gaza", "palestina", "israel", "hamas"], 
    "greece": ["gaza", "γκάζα", "παλαιστίνη", "israel", "ισραήλ", "χαμάς"], 
    "hungary": ["gaza", "palesztina", "izrael", "hamász"], 
    "austria": ["gaza", "palästina", "israel", "hamas"],  
    "switzerland": ["gaza", "palästina", "israel", "hamas"],  
    "ireland": ["gaza", "palestine", "israel", "hamas"], 
    "belgium": ["gaza", "palestine", "israel", "hamas"],
    "czech": ["gaza", "palestina", "izrael", "hamas"],  
    "romania": ["gaza", "palestina", "israel", "hamas"]  
}


results_comments = []
results_posts = []

def analyze_comments_from_post(post, subreddit_name, keyword):
    """Analizza tutti i commenti di un post"""
    try:
        post.comments.replace_more(limit=None)  # Carica commenti nested 
        
        comment_count = 0
        total_score = 0
        top_level_comments = 0
        
        for comment in post.comments.list():
            if isinstance(comment, praw.models.MoreComments):
                continue
                
            comment_count += 1
            total_score += comment.score
            
            # Commenti di primo livello (risposte dirette al post)
            if comment.is_root:
                top_level_comments += 1
            
            # Salva ogni commento individualmente 
            results_comments.append({
                'subreddit': subreddit_name,
                'post_id': post.id,
                'post_title': post.title[:100],  # Primi 100 caratteri
                'keyword_found': keyword,
                'comment_id': comment.id,
                'comment_body': comment.body[:200],  # Primi 200 caratteri
                'comment_score': comment.score,
                'comment_created': datetime.fromtimestamp(comment.created_utc),
                'is_top_level': comment.is_root,
                'parent_id': comment.parent_id,
                'post_score': post.score,
                'post_comments_total': post.num_comments,
                'data_raccolta': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return {
            'comment_count': comment_count,
            'avg_comment_score': total_score / comment_count if comment_count > 0 else 0,
            'top_level_comments': top_level_comments
        }
        
    except Exception as e:
        print(f"      Errore nell'analisi commenti: {e}")
        return {'comment_count': 0, 'avg_comment_score': 0, 'top_level_comments': 0}

print("Inizio analisi COMMENTI sui post relativi a Gaza...")
print("=" * 60)

for sub, keywords in keywords_by_country.items():
    print(f"\nAnalizzando COMMENTI in r/{sub}...")
    total_comments_nations = 0
    for keyword in keywords:
        try:
            time.sleep(1.5)
            
            subreddit = reddit.subreddit(sub)
            post_count = 0
            total_comments_analyzed = 0
            
            print(f"Cercando post con: '{keyword}'")
            
            # Trova post con la keyword
            for post in subreddit.search(keyword,limit = None, time_filter="year"):  # Limite None
                # Verifica che il post sia rilevante
                content = f"{post.title} {post.selftext}".lower()
                if any(kw in content for kw in keywords):
                    post_count += 1
                    print("numero post analizzati --> ", post_count,";   subreddit: r/", subreddit, ";   keyword: ", keyword)
                    
                    #print(f"     Post: '{post.title[:50]}...' ({post.num_comments} commenti)")
                    
                    # Analizza i commenti di questo post
                    comment_stats = analyze_comments_from_post(post, sub, keyword)
                    total_comments_analyzed += comment_stats['comment_count']
                    
                    # Salva statistiche del post
                    results_posts.append({
                        'subreddit': sub,
                        'keyword': keyword,
                        'post_id': post.id,
                        'post_title': post.title[:100],
                        'post_score': post.score,
                        'post_comments_total': post.num_comments,
                        'post_created': datetime.fromtimestamp(post.created_utc),
                        'comments_analyzed': comment_stats['comment_count'],
                        'avg_comment_score': comment_stats['avg_comment_score'],
                        'top_level_comments': comment_stats['top_level_comments'],
                        'data_raccolta': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
            
            print(f"-----> '{keyword}': {post_count} post analizzati, {total_comments_analyzed} commenti totali")
            total_comments_nations += total_comments_analyzed
            
        except Exception as e:
            print(f"Errore con '{keyword}': {e}")
            continue
    print (f"commenti totali per {sub}  --> ", total_comments_nations)
# Salva risultati
timestamp = datetime.now().strftime("%Y%m%d_%H%M")

if results_comments:
    df_comments = pd.DataFrame(results_comments)
    df_comments.to_csv(f"dataset_commenti_PROVA{timestamp}.csv", index=False, encoding='utf-8')
    print(f"\n ---> Commenti salvati: dataset_commenti_PROVA_{timestamp}.csv")
    print(f" ---> Totale commenti analizzati: {len(df_comments)}")

if results_posts:
    df_posts = pd.DataFrame(results_posts)
    df_posts.to_csv(f"dataset_post_PROVA{timestamp}.csv", index=False)
    print(f"\n ---> Post salvati: dataset_post_PROVA_{timestamp}.csv")
    print(f" ---> Totale post analizzati: {len(df_posts)}")

# Statistiche finali
if results_posts:
    total_posts = len(results_posts)
    total_comments = len(results_comments)
    avg_comments_per_post = total_comments / total_posts if total_posts > 0 else 0
    
    print(f"\n" + "=" * 60)
    print(f" ANALISI COMMENTI COMPLETATA!")
    print(f" STATISTICHE FINALI:")
    print(f"   > Subreddit analizzati: {len(keywords_by_country)}")
    print(f"   > Post analizzati: {total_posts}")
    print(f"   > Commenti analizzati: {total_comments}")
    print(f"   > Commenti per post (media): {avg_comments_per_post:.1f}")
    
    # Top subreddit per engagement
    engagement_stats = df_posts.groupby('subreddit').agg({
        'post_comments_total': 'sum',
        'post_score': 'sum',
        'post_id': 'count'
    }).round(1)
    
    engagement_stats.columns = ['commenti_totali', 'score_totale', 'numero_post']
    engagement_stats['engagement_medio'] = engagement_stats['commenti_totali'] / engagement_stats['numero_post']
    
    print(f"\nCLASSIFICA ENGAGEMENT:")
    print(engagement_stats.sort_values('engagement_medio', ascending=False))