# AI-Chat-Agent

## 프로젝트 개요
* AI Chat Agent 프로젝트는 최신 LLM 생태계를 활용한 대화형 정보 탐색 시스템입니다. 
* 사용자 질문에 대해 외부 정보를 종합하고, 추론 기반의 응답을 제공하는 지능형 대화 시스템입니다. 다음의 특징을 중심으로 설계됩니다.
  * Hexagonal Architecture 기반 설계로 높은 유연성과 유지보수성을 확보
  * Kafka 기반 비동기 메시징을 통한 마이크로서비스 연동
  * LangChain, LangGraph, MCP 등을 통해 에이전트 워크플로우를 구현
  * Reasoning 및 참조 투명성 확보
    * 질문의 의도를 파악하고 사고 흐름을 추론 가능
    * 외부 문서(PDF, 뉴스 등)를 웹이나 DB로 부터 수집하여 근거 기반 응답 제공
    * 사용된 정보의 출처와 우선순위를 명확히 표현
* 도메인을 AI 관련한 지식 정보 시스템으로 선정하고 구현합니다.
  * AI 관련 논문 또는 블로그, 뉴스 등의 데이터를 통해 질문에 대한 정보를 제공하는 것을 목적으로 합니다.

## 아키텍처 개요
### 1. 전체 구조
* TBD - 그림으로 추후 표현 합니다.(TBD, 브레인 스토밍/기술 탐색 단계)
    ```text
    [사용자] ──> [UI/REST] ──> [Agent 시스템] ──> [Kafka] ──> [문서처리 모듈 / LLM 응답 모듈]
                                              │
                                              └────> [Vector DB / Embedding / Reranker]
    ```
### 2. 시스템 구성 기슬 스택(TBD, 브레인 스토밍/기술 탐색 단계)

| **기능 범주**            | **기능 요소**                | **사용 기술**                                      |
|----------------------|------------------------|------------------------------------------------|
| **데이터 처리**           | 데이터 수집                 | Scrapy, 수동 스크랩                                 |
|                      | 데이터 저장                 | MariaDB, MongoDB, ElasticSearch                |
|                      | ORM                    | SQLAlchemy                                     |
| **RAG 구성요소**         | 텍스트 분할 (Text Splitter) | RecursiveCharacter, Markdown Splitter 등 |
|                      | 임베딩 (Embedding)        | HuggingFace, OpenAI, FastText                  |
|                      | 벡터 저장소 (Vector Store)  | FAISS, Chroma, Weaviate                        |
|                      | 검색기 (Retriever)        | LangChain Retriever, Custom Retriever 등        |
|                      | 리랭커 (Reranker)         | BM25, DenseRetriever, HybridReranker           |
| **RAG 엔진**           | RAG 파이프라인              | LangChain, LangGraph, LangSmith                |
| **메시징 처리**           | 메시징 브로커                | Apache Kafka                                   |
| **MCP (Context 관리)** | Context Protocol       | Model Context Protocol (MCP)                   |
| **LLM 처리**           | LLM 엔진                 | OpenAI GPT-4o-mini, Meta LLaMA 3.1             |
| **사용자 인터페이스**        | Web 프레임워크              | FastAPI, Streamlit, Gradio                     |
| **UI/UX 플랫폼**        | 사용자 인터랙션               | Gradio (LLM 응답 시각화), Streamlit (Demo 기반)       |
| **테스트 및 품질보장**       | 테스트 프레임워크              | Pytest (단위/통합 테스트 구성)                          |
### 3. 설계
1. Hexagonal Architecture
   * 선정 이유
     * 확장성
       * AI Agent는 다양한 외부 시스템(API, DB, Vector Store 등)과 연동되며, 변경 가능성이 높습니다.
       * Hexagonal 구조는 각 기능을 어댑터 형태로 캡슐화하여 외부 시스템 교체 시에도 내부 도메인 영향 없이 확장할 수 있습니다.
     * 유지보수성
       * 핵심 비즈니스 로직을 담당하는 도메인 영역과, 기술 종속이 강한 어댑터 영역을 분리하여 기술 스택의 업그레이드 또는 교체에 유연하게 대응할 수 있습니다.
     * 테스트 용이성
       * 도메인과 어댑터가 포트(Interface)로 분리되어 있기 때문에, 테스트 시에는 실제 구현 대신 Mock 어댑터를 주입하여 독립적인 유닛 테스트를 수행할 수 있습니다.
       * 각 계층은 **단일 책임 원칙(SRP)**에 따라 기능이 분리되므로 테스트 커버리지 확보에 용이합니다.
    * 기대 효과
      * 도메인 중심의 설계로 인해 비즈니스 로직의 일관성과 가독성 향상
      * 다수의 외부 시스템을 다루는 AI 시스템 구조에 적합
      * 에이전트 워크플로우의 유연한 교체 및 확장 가능성 확보
2. 웹 프레임워크 설계 전략
   * 핵심 방향
     * 비동기 처리 지원 (Async I/O): 사용자 요청과 LLM 응답 간 대기 시간이 길 수 있으므로, 비동기 기반 처리를 통해 응답 지연을 최소화하고 리소스 효율을 높입니다.
     * 멀티프로세싱 구조: 대규모 문서 파싱, 임베딩 처리, RAG 호출 등의 작업은 병렬 수행이 요구되므로, 멀티프로세싱 기반 Task 분산 처리 구조를 도입합니다.
     * Job Manager 연동: 각 요청의 중요도 또는 긴급도에 따라 우선순위를 지정하고 큐에 등록하여 백그라운드에서 비동기 실행할 수 있도록 Job Manager를 구성합니다.
   * 기대 효과
     * 빠른 요청 응답 
     * 대규모 문서 처리 환경에서의 병목 완화
     * 우선순위 기반 작업 분배로 서버 부하 분산 및 안정성 확보
3. Kafka 기반 Microservice 메시징 구조
   * 선정 이유
     * Kafka는 고성능 메시지 브로커로서 비동기 처리, 느슨한 결합, 분산 확장성 확보에 적합합니다.
     * 각 기능(문서 처리, 임베딩, 검색, 응답 등)을 마이크로서비스 형태로 분리하여, Kafka를 통해 메시지를 주고받는 구조로 설계합니다.
   * 구성 방식
     * 각 서비스는 토픽 기반의 메시지 소비자(Consumer)로 동작
     * Kafka 토픽은 기능 단위로 구분 (예: doc.ingest, rag.search, llm.answer)
     * 실패한 메시지는 Dead Letter Queue로 분리 저장하여 재처리 가능
   * 기대 효과
     * 시스템 구성 요소 간 완전한 독립성과 비동기 실행 확보
     * 고가용성(HA) 아키텍처 구성 기반 확보
     * 향후 스케일아웃 및 멀티 서비스 확장 용이

## 구체적 설계 전략
### 1. Hexagonal Architecture
* 구성
  * Domain Hexagon
    * 설명 
      * 시스템의 핵심 비즈니스 로직을 담당하며 기술에 독립적인 POJO(Plain Old Java Object)로 구성
      * Entity, VO(Enum 포함), Aggregate, Utility, Extension, Constants를 포함하여 비지니스 로직을 작성
      * 외부 라이브러리(Spring 등)에 의존하지 않음
    * 구성
        * TBD
  * Application Hexagon
    * 설명
      * 도메인 헥사곤을 사용하여 시스템이 가지는 기능/사례(usecase)를 정의
      * 도메인의 유즈케이스(UseCase)를 관리하며 기술에 독립적 입니다.
      * usecase, outputPort(interface), logging, exception 등을 포함
      * 기술 세부사항(DB, 외부 API 등)에 대해 알 필요가 없으며, 부포트를 통해 의존성을 해결
      * 팀에 신규 인력이 추가되거나 더 나아가 PO(ProductOwner), PM(ProductManager) 같이 비 개발 인력도 읽을 수 있을만한 쉬운 코드로 작성
      * 의존성은 Domain Hexagon에 대해서만 가짐
    * 구성
      * DB
        * TBD
  * Framework Hexagon 
    * 애플리케이션의 진입점으로 주어댑터(Primary Adapter)를 통해 클라이언트 요청을 처리
    * Primary/Driving Adapters (User Interface) 영역
    * REST API, 메시지 컨슈머 등 외부 클라이언트와의 통신을 담당
    * Domain, Application, Framework Hexagon에 대하여 의존적, 애플리케이션 구동에 필요한 모듈의 config만 선별적으로 import
  * Bootstrap Hexagon : 데이터베이스, 외부 API 등 기반 요소를 처리하는 어댑터
    * 설명
      * 애플리케이션의 진입점으로 주어댑터(Primary Adapter)를 통해 클라이언트 요청을 처리
      * Primary/Driving Adapters (User Interface) 영역
      * REST API, 메시지 컨슈머 등 외부 클라이언트와의 통신을 담당
      * Domain, Application, Framework Hexagon에 대하여 의존적, 애플리케이션 구동에 필요한 모듈의 config만 선별적으로 import
    * 구성
      * Streamlit
        * TBD
* 주의할 부분
  * 헥사곤 간 객체 변환 (핵사곤 간 데이터 이동 시)
    * DTO(Data Transfer Object)를 사용해 각 헥사곤의 데이터 형식을 정의
    * 도메인 객체 내부에 변환 메서드 포함
  * 인터페이스 증가
    * 외부 기술(DB, API 등)과의 연결을 위해 Output Port 인터페이스가 많아짐으로 중복 구현과 관리 복잡성이 증가
      * 공통 Port 설계: 비슷한 성격의 Output Port를 추상화하여 통합
        * ex) Spring Data JPA의 기본 리포지토리 인터페이스를 활용하면 CRUD 작업 인터페이스 중복을 최소화
  * 복잡한 설정 관리
    * 다양한 헥사곤의 컴포넌트를 초기화해야 하며, 모든 구성 요소를 일괄 로드하면 불필요한 의존성이 발생할 수 있음
      * 문제점 : 사용하지 않는 헥사곤의 컴포넌트까지 초기화되어 메모리와 실행 시간을 낭비
      * 해결 방법 : 헥사곤별로 설정 클래스를 분리하여 관리, Spring의 @Import와 @ComponentScan의 lazyInit 옵션을 활용해 필요한 컴포넌트만 로드
### 2.웹 프레임워크 설계 전략
* TBD
### 3. Kafka 기반 Microservice 메시징 구조
* TBD

## 구현 및 테스트 전략
1. 구현 시 원칙
    * 기능 구현 시 반드시 테스트 코드 포함
    * 외부 API 또는 Kafka 연동은 모킹 또는 통합 테스트로 검증
2. 테스트 전략

| 구분            | 내용                                                         |
| --------------- | ------------------------------------------------------------ |
| **단위 테스트** | 각 Hexagon의 UseCase 및 서비스 메서드 테스트 예: Retriever 동작 확인 |
| **통합 테스트** | Kafka 메시지 수신 → 처리 → 응답 흐름 전체 테스트 예: 전체 RAG 파이프라인 통합 실행 |
3. 구조 
    * TBD
    ```
    src/
    ├── domain/                # 도메인 헥사곤 (비즈니스 로직)
    ├── application/           # 애플리케이션 헥사곤 (유스케이스)
    ├── framework/             # 프레임워크 헥사곤 (DB, 외부 API)
    ├── bootstrap/             # 부트스트랩 헥사곤 (REST API, CLI)
    ```

## 성능 평가
* TBD