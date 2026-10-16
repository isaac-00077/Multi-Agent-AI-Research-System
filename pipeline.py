from agents import build_scrape_agent, build_search_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:

    state={}

    #search agent working
    print("\n"+" ="*50)
    print("step 1 - search agent is working ... ")
    print("="*50)

    search_agent=build_search_agent()
    search_result=search_agent.invoke({
        "messages": [("user",
            f"""
                Find Find recent, reliable and detailed information about: {topic}

                Use the web_search tool.
                Call it with the required query argument containing
                the complete research topic.

            """)]
    })

    state["search_result"]=search_result['messages'][-1].content

    print("\n search result ",state['search_result'])

     #step 2 - reader agent 
    print("\n"+" ="*50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("="*50)

    reader_agent=build_scrape_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_result'][:800]}"
        )]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    #step 3 - writer chain 

    print("\n"+" ="*50)
    print("step 3 - Writer is drafting the report ...")
    print("="*50)


    research_combined = (
        f"SEARCH RESULTS : \n {state['search_result']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    state['report'] = writer_chain.invoke({
        "topic":topic,
        "research":research_combined
    })

    print("\n Final Report\n",state['report'])

    #critic report 

    print("\n"+" ="*50)
    print("step 4 - critic is reviewing the report ")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })

    print("\n critic report \n", state['feedback'])

    return state

def run_research_pipeline_stream(topic: str):
    """
    Generator that executes the multi-agent research pipeline step-by-step
    and yields real-time progress events for the WebGL UI.
    """
    state = {}

    # STEP 1: Search Agent
    yield {
        "step": 1,
        "agent": "search",
        "status": "active",
        "message": f"Search Agent initiated. Deploying web_search (Tavily) for topic: '{topic}'"
    }
    
    try:
        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user",
                f"Find recent, reliable and detailed information about: {topic}\n\n"
                f"Use the web_search tool.\n"
                f"Call it with the required query argument containing the complete research topic.\n"
            )]
        })
        state["search_result"] = search_result['messages'][-1].content
    except Exception as e:
        state["search_result"] = f"Error during search: {str(e)}"

    yield {
        "step": 1,
        "agent": "search",
        "status": "done",
        "message": f"Search Agent completed. Gathered {len(state['search_result'])} characters of web intelligence.",
        "data": state["search_result"]
    }

    # STEP 2: Reader / Scraper Agent
    yield {
        "step": 2,
        "agent": "scrape",
        "status": "active",
        "message": "Reader Agent analyzing search results to select and scrape primary source..."
    }

    try:
        reader_agent = build_scrape_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_result'][:800]}"
            )]
        })
        state['scraped_content'] = reader_result['messages'][-1].content
    except Exception as e:
        state['scraped_content'] = f"Error during scraping: {str(e)}"

    yield {
        "step": 2,
        "agent": "scrape",
        "status": "done",
        "message": f"Reader Agent extracted {len(state['scraped_content'])} characters of deep text content.",
        "data": state["scraped_content"]
    }

    # STEP 3: Writer Chain
    yield {
        "step": 3,
        "agent": "writer",
        "status": "active",
        "message": "Writer Agent synthesizing intelligence into structured 4-part research report..."
    }

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_result']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    try:
        state['report'] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined
        })
    except Exception as e:
        state['report'] = f"Error during report writing: {str(e)}"

    yield {
        "step": 3,
        "agent": "writer",
        "status": "done",
        "message": "Writer Agent finished full report draft.",
        "data": state["report"]
    }

    # STEP 4: Critic Chain
    yield {
        "step": 4,
        "agent": "critic",
        "status": "active",
        "message": "Critic Agent stress-testing claims and evaluating score / verdict..."
    }

    try:
        state["feedback"] = critic_chain.invoke({
            "report": state['report']
        })
    except Exception as e:
        state["feedback"] = f"Error during critique: {str(e)}"

    yield {
        "step": 4,
        "agent": "critic",
        "status": "done",
        "message": "Critic Agent completed evaluation.",
        "data": state["feedback"]
    }

    # STEP 5: Final Completion
    yield {
        "step": 5,
        "agent": "core",
        "status": "complete",
        "message": "Research pipeline execution complete. Dossier ready for inspection.",
        "state": state
    }

if __name__=="__main__":
    topic = input("\nEnter a research topic : ")
    run_research_pipeline(topic)