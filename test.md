# Activity 1 — Agent Dialogue with KQML & KIF

**Activity Type:** Practical (Agent Communication)  
**Theme/Topic:** KQML performatives with KIF content for warehouse querying  
**Related Learning Outcomes:**  
- Understand motivations for—and appropriate use of—agent-based computing.  
- Understand main agent models and their grounding in AI research.

## Summary of Activity
I implemented a short dialogue between **Alice** (procurement) and **Bob** (warehouse) using **KQML** performatives with **KIF** content. Alice queried (i) available stock of 50-inch televisions and (ii) the number of HDMI slots. Bob replied with `tell` messages carrying bindings (e.g., `(= ?qty 42)`). The example separates protocol (KQML) from semantics (KIF) and demonstrates intent-centric messaging for interoperable multi-agent systems.

## Key Concepts & Insights
- **Protocol vs. semantics:** KQML handles *how* agents talk; KIF captures *what* they assert.  
- **Ontology hygiene:** agreeing on symbols like `tv-50-inch` and `hdmi-slots` avoids drift.  
- **Testable pairs:** compact **ask-one / tell** exchanges validate messaging and KB consistency.

## Critical Reflection
Defining precise KIF predicates reduced ambiguity in replies. Next, I’d add error paths (unknown item, unit mismatch) and negotiation for alternatives when stock is low.



# Activity 2 — Constituency Parse Trees

**Activity Type:** Practical (NLP Syntax)  
**Theme/Topic:** Constituency-based parsing (Penn Treebank style)  
**Related Learning Outcomes:**  
- Develop, deploy and evaluate intelligent-systems techniques for real problems.  
- Understand contemporary research issues in intelligent agent systems (language understanding as capability).

## Summary of Activity
I produced Penn Treebank–style constituency trees for:  
1) *The government raised interest rates.*  
2) *The internet gives everyone a voice.*  
3) *The man saw the dog with the telescope.* — using the **VP-attachment** reading (PP modifies *saw*).  
Each tree was exported as text and rendered to PNG for portfolio evidence.

## Key Concepts & Insights
- **Hierarchy:** Sentences decompose into S → NP/VP/PP constituents with POS tags.  
- **Attachment:** Prepositional phrases create structural ambiguity; choosing VP-attachment changes interpretation.  
- **Explainability:** Explicit trees clarify where parsers need statistical/semantic cues.

## Critical Reflection
Manually building trees highlighted ambiguity hotspots. Next, I’d compare a PCFG/neural parser’s outputs against these “gold” trees and analyse attachment decisions.

## Evidence (Artefacts)


# Activity 3 — Deep Learning in Biomedicine: Societal Impact

**Activity Type:** Research Discussion  
**Theme/Topic:** Deep learning for -omics & imaging  
**Related Learning Outcomes:**  
- Apply intelligent-systems techniques to real problems.  
- Understand contemporary issues and socio-technical impacts of AI systems.

Deep learning is transforming biomedicine by extracting high‑level representations from large, heterogeneous -omics and imaging datasets and enabling advances in biomarker discovery, genomics, transcriptomics, proteomics, structural biology, and drug discovery (Mamoshina et al., 2016). Convolutional neural networks, autoencoders, deep belief networks, and recurrent architectures provide powerful tools for feature extraction, cross‑platform generalization, and prediction tasks that traditional methods struggle with, such as annotating gene expression images, predicting noncoding variant effects, and modeling drug‑target interactions (Mamoshina et al., 2016). These methods reduce manual feature engineering, allow multimodal integration of genome/transcriptome/proteome/drug data, and have produced state‑of‑the‑art results across many benchmark tasks and datasets (Mamoshina et al., 2016). Limitations remain: models are often “black boxes,” require large curated datasets and significant computational resources, and demand careful hyperparameter optimization to avoid overfitting (Mamoshina et al., 2016). Ethical and socio‑technical implications include risks from biased or nonrepresentative training data, challenges for clinical interpretability and regulatory approval, and potential shifts in research and industry labor. Responsible deployment requires interpretability techniques, rigorous validation on independent cohorts, transparent reporting, and close collaboration between biologists, clinicians, and machine‑learning experts to translate technical gains into safe, equitable biomedical benefits (Mamoshina et al., 2016).

## References:

Mamoshina, P., Vieira, A., Putin, E. and Zhavoronkov, A., 2016. Applications of deep learning in biomedicine. Molecular Pharmaceutics, 13, pp.1445–1454. doi:10.1021/acs.molpharmaceut.5b00982.
