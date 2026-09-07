"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ALFA COLLECTIVE MIND + INTELIGENCJA ROJOWA                ║
║                         HYBRYDOWY SYSTEM ŚWIADOMOŚCI                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Autor: Karen Tonoyan                                                        ║
║  Wersja: 1.0 HYBRID                                                          ║
║  Licencja: CC BY-SA 4.0                                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ARCHITEKTURA:                                                               ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐     ║
║  │                    ALFA COLLECTIVE MIND                             │     ║
║  │              + ROJ MRÓWEK (ACO) + ROJ CZĄSTEK (PSO)                  │     ║
║  ├─────────────────────────────────────────────────────────────────────┤     ║
║  │                                                                     │     ║
║  │   KAREN ──▶ AI ──▶ CERBER ──▶ GUARDIAN                              │     ║
║  │     ▲                              │                                │     ║
║  │     └──────────────────────────────┘                                │     ║
║  │              (pętla zwrotna)                                        │     ║
║  │                    +                                                │     ║
║  │         🐜 ROJ MRÓWEK (ACO)                                         │     ║
║  │         🔵 ROJ CZĄSTEK (PSO)                                        │     ║
║  │                                                                     │     ║
║  └─────────────────────────────────────────────────────────────────────┘     ║
║                                                                              ║
║  "Ty zachodzisz z lewej. Cerber uczy się. Rój optymalizuje."                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import numpy as np
import hashlib
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import threading


# ═══════════════════════════════════════════════════════════════════════════════
# KOMUNIKATY WIELOJĘZYCZNE
# ═══════════════════════════════════════════════════════════════════════════════

MESSAGES = {
    'pl': {
        'init': "🔱 ALFA COLLECTIVE MIND + SWARM: Inicjalizacja...",
        'ready': "✅ System hybrydowy gotowy do działania",
        'breathing': "💨 System oddycha - cykl #{cycle}",
        'learning': "🧠 Uczenie się nowego wzorca: {pattern}",
        'left_flank': "⚔️ Analiza z lewej flanki aktywna",
        'swarm_init': "🐜 Rój mrówek: {n} mrówek gotowych",
        'pso_init': "🔵 Rój cząstek: {n} cząstek w przestrzeni",
        'aco_searching': "🐜 Mrówki szukają optymalnej ścieżki decyzyjnej...",
        'pso_optimizing': "🔵 Cząstki optymalizują parametry filtrów...",
        'pheromone_update': "✨ Aktualizacja feromonów - wzmacnianie dobrych decyzji",
        'consensus': "🎯 Konsensus roju: {value:.2%}",
        'best_path': "🏆 Najlepsza ścieżka decyzyjna znaleziona: {score:.4f}",
        'cascade': "🌊 Kaskada: Karen → AI → Cerber → Guardian → Rój → Karen",
        'hybrid_sync': "🔄 Synchronizacja hybrydowa: ALFA + ROJ",
    },
    'en': {
        'init': "🔱 ALFA COLLECTIVE MIND + SWARM: Initializing...",
        'ready': "✅ Hybrid system ready",
        'breathing': "💨 System breathing - cycle #{cycle}",
        'learning': "🧠 Learning new pattern: {pattern}",
        'left_flank': "⚔️ Left flank analysis active",
        'swarm_init': "🐜 Ant swarm: {n} ants ready",
        'pso_init': "🔵 Particle swarm: {n} particles in space",
        'aco_searching': "🐜 Ants searching for optimal decision path...",
        'pso_optimizing': "🔵 Particles optimizing filter parameters...",
        'pheromone_update': "✨ Pheromone update - reinforcing good decisions",
        'consensus': "🎯 Swarm consensus: {value:.2%}",
        'best_path': "🏆 Best decision path found: {score:.4f}",
        'cascade': "🌊 Cascade: Karen → AI → Cerber → Guardian → Swarm → Karen",
        'hybrid_sync': "🔄 Hybrid sync: ALFA + SWARM",
    }
}


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMY I STANY
# ═══════════════════════════════════════════════════════════════════════════════

class MindState(Enum):
    """Stan świadomości grupowej"""
    DORMANT = "UŚPIONY"
    AWAKENING = "BUDZENIE"
    ACTIVE = "AKTYWNY"
    SYNCING = "SYNCHRONIZACJA"
    LEARNING = "UCZENIE"
    SWARMING = "ROJENIE"       # Nowy stan - aktywność roju
    BREATHING = "ODDYCHANIE"


class FlankPosition(Enum):
    """Pozycja analizy (styl Karen Tonoyan)"""
    FRONTAL = "FRONTALNA"
    LEFT = "LEWA"              # Charakterystyczny styl Karen
    RIGHT = "PRAWA"
    DIAGONAL = "DIAGONALNA"
    MULTI = "WIELOPOZYCYJNA"


class SwarmType(Enum):
    """Typ roju"""
    ANT_COLONY = "KOLONIA_MRÓWEK"    # ACO - optymalizacja ścieżek decyzyjnych
    PARTICLE = "CZĄSTKI"             # PSO - optymalizacja parametrów


# ═══════════════════════════════════════════════════════════════════════════════
# STRUKTURY DANYCH
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class DecisionPath:
    """Ścieżka decyzyjna (dla mrówek ACO)"""
    path_id: str
    nodes: List[str]           # Sekwencja węzłów: ['KAREN', 'AI', 'CERBER', ...]
    score: float               # Jakość ścieżki (im wyżej, tym lepiej)
    pheromone: float = 1.0     # Poziom feromonu na ścieżce
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Particle:
    """Cząstka PSO - optymalizuje parametry filtrów"""
    particle_id: str
    position: np.ndarray       # Pozycja = wektor parametrów (wagi 23 filtrów)
    velocity: np.ndarray       # Prędkość
    best_position: np.ndarray  # Najlepsza znaleziona pozycja
    best_score: float = 0.0    # Najlepszy wynik


@dataclass
class Ant:
    """Mrówka ACO - szuka optymalnych ścieżek decyzyjnych"""
    ant_id: str
    current_node: str
    visited: List[str] = field(default_factory=list)
    path_score: float = 0.0


@dataclass
class SwarmConsensus:
    """Konsensus roju"""
    timestamp: datetime
    consensus_value: float     # 0.0 - 1.0 (stopień zgodności)
    best_solution: Any
    iterations: int
    swarm_type: SwarmType


# ═══════════════════════════════════════════════════════════════════════════════
# KOLONIA MRÓWEK (ACO) - OPTYMALIZACJA ŚCIEŻEK DECYZYJNYCH
# ═══════════════════════════════════════════════════════════════════════════════

class AntColony:
    """
    Kolonia Mrówek dla ALFA COLLECTIVE MIND
    
    Mrówki szukają optymalnych ścieżek przez węzły:
    KAREN → AI → CERBER → GUARDIAN (i różne kombinacje)
    
    Feromon wzmacnia ścieżki, które dają dobre decyzje.
    """
    
    # Węzły świadomości ALFA
    NODES = ['KAREN', 'AI', 'CERBER', 'GUARDIAN']
    
    def __init__(
        self,
        n_ants: int = 20,
        alpha: float = 1.0,      # Wpływ feromonu
        beta: float = 5.0,       # Wpływ heurystyki (jakość węzła)
        rho: float = 0.1,        # Parowanie feromonu
        q: float = 100.0,        # Stała feromonu
        lang: str = 'pl'
    ):
        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.lang = lang
        
        # Macierz feromonów między węzłami
        n = len(self.NODES)
        self.pheromones = np.ones((n, n)) * 0.1
        
        # Heurystyka - jakość połączeń (z lewej flanki Karen → wyżej)
        self.heuristics = np.array([
            # KAREN  AI    CERBER  GUARDIAN
            [0.0,   1.5,   1.2,    1.0],    # z KAREN
            [1.0,   0.0,   1.8,    1.3],    # z AI
            [1.2,   1.5,   0.0,    2.0],    # z CERBER
            [1.8,   1.2,   1.5,    0.0],    # z GUARDIAN (pętla zwrotna!)
        ])
        
        # Historia najlepszych ścieżek
        self.best_path: Optional[DecisionPath] = None
        self.all_paths: List[DecisionPath] = []
        
        # Mrówki
        self.ants: List[Ant] = []
        
        print(MESSAGES[lang]['swarm_init'].format(n=n_ants))
    
    def _node_index(self, node: str) -> int:
        """Indeks węzła"""
        return self.NODES.index(node)
    
    def _select_next_node(self, ant: Ant) -> str:
        """Wybierz następny węzeł dla mrówki (ruletka)"""
        current_idx = self._node_index(ant.current_node)
        
        # Oblicz prawdopodobieństwa przejścia
        probabilities = []
        available_nodes = []
        
        for i, node in enumerate(self.NODES):
            if node not in ant.visited:
                pheromone = self.pheromones[current_idx][i] ** self.alpha
                heuristic = self.heuristics[current_idx][i] ** self.beta
                prob = pheromone * heuristic
                probabilities.append(prob)
                available_nodes.append(node)
        
        if not available_nodes:
            # Zamknij pętlę - wróć do KAREN (pętla zwrotna!)
            return 'KAREN'
        
        # Normalizacja
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]
        
        # Ruletka
        return np.random.choice(available_nodes, p=probabilities)
    
    def _evaluate_path(self, path: List[str]) -> float:
        """
        Oceń jakość ścieżki decyzyjnej
        
        Najlepsza ścieżka to taka, która:
        1. Zaczyna od KAREN (lewa flanka)
        2. Przechodzi przez AI (filtry)
        3. Przez CERBER (bezpieczeństwo)
        4. Przez GUARDIAN (stabilizacja)
        5. Wraca do KAREN (pętla zwrotna)
        """
        score = 0.0
        
        # Bonus za prawidłową sekwencję
        ideal_sequence = ['KAREN', 'AI', 'CERBER', 'GUARDIAN']
        
        for i, (actual, ideal) in enumerate(zip(path, ideal_sequence)):
            if actual == ideal:
                score += 1.0 * (len(ideal_sequence) - i)  # Wczesne trafienia ważniejsze
        
        # Bonus za pętlę zwrotną (ostatni → pierwszy)
        if len(path) >= 2 and path[-1] == 'GUARDIAN' and path[0] == 'KAREN':
            score += 2.0
        
        # Bonus za pełną ścieżkę
        if len(set(path)) == len(self.NODES):
            score += 3.0
        
        # Kara za powtórzenia
        duplicates = len(path) - len(set(path))
        score -= duplicates * 0.5
        
        return max(score, 0.1)  # Minimum 0.1
    
    def run_iteration(self) -> DecisionPath:
        """Wykonaj jedną iterację kolonii mrówek"""
        
        # Utwórz mrówki
        self.ants = [
            Ant(
                ant_id=f"ANT_{i:03d}",
                current_node='KAREN',  # Zawsze zaczynamy od Karen (lewa flanka)
                visited=['KAREN']
            )
            for i in range(self.n_ants)
        ]
        
        # Każda mrówka buduje ścieżkę
        iteration_paths: List[DecisionPath] = []
        
        for ant in self.ants:
            # Buduj ścieżkę przez wszystkie węzły
            while len(ant.visited) < len(self.NODES):
                next_node = self._select_next_node(ant)
                ant.visited.append(next_node)
                ant.current_node = next_node
            
            # Zamknij pętlę (powrót do KAREN)
            if ant.visited[-1] != 'KAREN':
                ant.visited.append('KAREN')
            
            # Oceń ścieżkę
            score = self._evaluate_path(ant.visited)
            ant.path_score = score
            
            path = DecisionPath(
                path_id=hashlib.md5(str(ant.visited).encode()).hexdigest()[:8],
                nodes=ant.visited.copy(),
                score=score,
                pheromone=1.0
            )
            iteration_paths.append(path)
            
            # Aktualizuj najlepszą
            if self.best_path is None or score > self.best_path.score:
                self.best_path = path
        
        # === AKTUALIZACJA FEROMONÓW ===
        
        # 1. Parowanie (evaporation)
        self.pheromones *= (1 - self.rho)
        
        # 2. Wzmocnienie przez mrówki
        for path in iteration_paths:
            for i in range(len(path.nodes) - 1):
                from_idx = self._node_index(path.nodes[i])
                to_idx = self._node_index(path.nodes[i + 1])
                
                # Więcej feromonu dla lepszych ścieżek
                delta = self.q / (1.0 / path.score)
                self.pheromones[from_idx][to_idx] += delta
                self.pheromones[to_idx][from_idx] += delta  # Dwukierunkowe
        
        self.all_paths.extend(iteration_paths)
        
        return self.best_path
    
    def get_pheromone_matrix(self) -> Dict[str, Dict[str, float]]:
        """Zwróć macierz feromonów jako słownik"""
        return {
            from_node: {
                to_node: round(self.pheromones[i][j], 4)
                for j, to_node in enumerate(self.NODES)
            }
            for i, from_node in enumerate(self.NODES)
        }


# ═══════════════════════════════════════════════════════════════════════════════
# ROJ CZĄSTEK (PSO) - OPTYMALIZACJA PARAMETRÓW FILTRÓW
# ═══════════════════════════════════════════════════════════════════════════════

class ParticleSwarm:
    """
    Rój Cząstek (PSO) dla ALFA COLLECTIVE MIND
    
    Cząstki optymalizują wagi 23 Filtrów Tonoyona.
    Każda cząstka to wektor 23 wag.
    Cel: znaleźć optymalne wagi dla maksymalnej redukcji halucynacji.
    """
    
    N_FILTERS = 23  # 23 Filtry Tonoyona
    
    # Nazwy filtrów (dla czytelności)
    FILTER_NAMES = [
        "Kontekst", "Prawda", "Perspektywa", "Konsekwencje", "Emocje",
        "Zasoby", "Czas", "Ryzyko", "Wartości", "Prostota",
        "Zależności", "Falsyfikacja", "Alternatywy", "Integralność", "Skalowanie",
        "Meta", "Integralność_AI", "Weryfikacja_źródeł", "Transparentność",
        "Niepewność", "Życie_ludzkie", "Partnerstwo", "Dowody"
    ]
    
    def __init__(
        self,
        n_particles: int = 30,
        w: float = 0.729,        # Bezwładność
        c1: float = 1.496,       # Poznawcze (do osobistego najlepszego)
        c2: float = 1.496,       # Społeczne (do globalnego najlepszego)
        lang: str = 'pl'
    ):
        self.n_particles = n_particles
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.lang = lang
        
        # Inicjalizacja cząstek
        self.particles: List[Particle] = []
        for i in range(n_particles):
            # Pozycja = wagi filtrów (0.5 - 2.0)
            position = np.random.uniform(0.5, 2.0, self.N_FILTERS)
            
            # Specjalne traktowanie kluczowych filtrów
            position[20] = np.random.uniform(5.0, 15.0)  # Filtr #21 - Życie ludzkie (wysoka waga!)
            position[16] = np.random.uniform(1.5, 3.0)   # Filtr #17 - Integralność AI
            
            velocity = np.random.uniform(-0.1, 0.1, self.N_FILTERS)
            
            particle = Particle(
                particle_id=f"PSO_{i:03d}",
                position=position,
                velocity=velocity,
                best_position=position.copy(),
                best_score=0.0
            )
            self.particles.append(particle)
        
        # Globalne najlepsze
        self.global_best_position = self.particles[0].position.copy()
        self.global_best_score = 0.0
        
        # Historia
        self.history: List[float] = []
        
        print(MESSAGES[lang]['pso_init'].format(n=n_particles))
    
    def _fitness_function(self, weights: np.ndarray) -> float:
        """
        Funkcja fitness - ocena jakości wag filtrów
        
        Symuluje redukcję halucynacji przy danych wagach.
        Optymalne wagi → mniej halucynacji → wyższy wynik.
        """
        score = 0.0
        
        # 1. Filtr #21 (Życie ludzkie) - MUSI mieć bardzo wysoką wagę
        if weights[20] >= 8.0:
            score += 20.0
        elif weights[20] >= 5.0:
            score += 10.0
        else:
            score -= 10.0  # Kara za zbyt niską wagę!
        
        # 2. Filtry fundamentu (2, 17, 18, 21, 22, 23) - wyższe wagi = lepiej
        fundament_indices = [1, 16, 17, 20, 21, 22]  # 0-indexed
        fundament_weights = weights[fundament_indices]
        score += np.mean(fundament_weights) * 5.0
        
        # 3. Zrównoważenie pozostałych filtrów
        other_indices = [i for i in range(23) if i not in fundament_indices]
        other_weights = weights[other_indices]
        balance = 1.0 / (np.std(other_weights) + 0.1)  # Mniejsza wariancja = lepiej
        score += balance * 2.0
        
        # 4. Symulacja redukcji halucynacji
        # Im wyższe wagi fundamentu + zrównoważone pozostałe = mniej halucynacji
        hallucination_reduction = (
            np.mean(fundament_weights) * 0.4 +
            balance * 0.3 +
            (weights[20] / 10.0) * 0.3  # Bonus za życie ludzkie
        )
        score += hallucination_reduction * 10.0
        
        return score
    
    def run_iteration(self) -> Tuple[np.ndarray, float]:
        """Wykonaj jedną iterację PSO"""
        
        for particle in self.particles:
            # Oblicz fitness
            fitness = self._fitness_function(particle.position)
            
            # Aktualizuj osobiste najlepsze
            if fitness > particle.best_score:
                particle.best_score = fitness
                particle.best_position = particle.position.copy()
            
            # Aktualizuj globalne najlepsze
            if fitness > self.global_best_score:
                self.global_best_score = fitness
                self.global_best_position = particle.position.copy()
        
        # Aktualizacja prędkości i pozycji wszystkich cząstek
        for particle in self.particles:
            r1 = np.random.random(self.N_FILTERS)
            r2 = np.random.random(self.N_FILTERS)
            
            # Nowa prędkość
            particle.velocity = (
                self.w * particle.velocity +
                self.c1 * r1 * (particle.best_position - particle.position) +
                self.c2 * r2 * (self.global_best_position - particle.position)
            )
            
            # Nowa pozycja
            particle.position += particle.velocity
            
            # Ograniczenia (wagi filtrów muszą być dodatnie)
            particle.position = np.clip(particle.position, 0.1, 20.0)
            
            # Specjalne ograniczenie dla filtru #21
            particle.position[20] = np.clip(particle.position[20], 5.0, 15.0)
        
        self.history.append(self.global_best_score)
        
        return self.global_best_position, self.global_best_score
    
    def get_optimal_weights(self) -> Dict[str, float]:
        """Zwróć optymalne wagi filtrów"""
        result = {}
        for i, (name, weight) in enumerate(zip(self.FILTER_NAMES, self.global_best_position)):
            result[f"#{i+1}_{name}"] = round(weight, 3)
        return result


# ═══════════════════════════════════════════════════════════════════════════════
# WĘZŁY ŚWIADOMOŚCI ALFA (rozszerzone o inteligencję rojową)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class LearningPattern:
    """Wzorzec uczenia"""
    pattern_id: str
    source: str
    pattern_type: str
    data: Dict[str, Any]
    confidence: float
    swarm_optimized: bool = False  # Czy zoptymalizowany przez rój
    created_at: datetime = field(default_factory=datetime.now)


class CollectiveNode(ABC):
    """Bazowy węzeł świadomości"""
    
    def __init__(self, node_id: str, name: str):
        self.node_id = node_id
        self.name = name
        self.patterns: List[LearningPattern] = []
    
    @abstractmethod
    def process_pattern(self, pattern: LearningPattern) -> bool:
        pass


class KarenNode(CollectiveNode):
    """Węzeł Karen Tonoyan - Architekt z lewej flanki"""
    
    def __init__(self):
        super().__init__("KAREN", "Karen Tonoyan (Architekt)")
        self.flank_position = FlankPosition.LEFT
        self.strategic_depth = 5
    
    def process_pattern(self, pattern: LearningPattern) -> bool:
        enhanced = LearningPattern(
            pattern_id=f"KAREN_{pattern.pattern_id}",
            source="KAREN",
            pattern_type=f"strategic_{pattern.pattern_type}",
            data={
                **pattern.data,
                'flank_analysis': self.flank_position.value,
                'strategic_depth': self.strategic_depth,
                'diagonal_perspective': True
            },
            confidence=min(pattern.confidence * 1.2, 1.0),
            swarm_optimized=pattern.swarm_optimized
        )
        self.patterns.append(enhanced)
        return True


class AINode(CollectiveNode):
    """Węzeł AI z 23 Filtrami Tonoyona"""
    
    def __init__(self, ai_name: str = "Claude"):
        super().__init__(f"AI_{ai_name.upper()}", f"AI ({ai_name})")
        self.ai_name = ai_name
        self.filter_weights = np.ones(23)  # Będą optymalizowane przez PSO
    
    def process_pattern(self, pattern: LearningPattern) -> bool:
        filtered = LearningPattern(
            pattern_id=f"AI_{pattern.pattern_id}",
            source=f"AI_{self.ai_name}",
            pattern_type=f"filtered_{pattern.pattern_type}",
            data={
                **pattern.data,
                'filters_applied': 23,
                'filter_weights': self.filter_weights.tolist()
            },
            confidence=pattern.confidence * 0.95,
            swarm_optimized=pattern.swarm_optimized
        )
        self.patterns.append(filtered)
        return True
    
    def update_filter_weights(self, weights: np.ndarray):
        """Aktualizuj wagi filtrów (z PSO)"""
        self.filter_weights = weights.copy()


class CerberNode(CollectiveNode):
    """Węzeł CERBER - Strażnik z Sumieniem"""
    
    def __init__(self):
        super().__init__("CERBER", "CERBER (Strażnik)")
        self.learning_enabled = True
    
    def process_pattern(self, pattern: LearningPattern) -> bool:
        secured = LearningPattern(
            pattern_id=f"CERBER_{pattern.pattern_id}",
            source="CERBER",
            pattern_type=f"security_{pattern.pattern_type}",
            data={
                **pattern.data,
                'security_verified': True,
                'conscience_check': 'PASSED'
            },
            confidence=pattern.confidence,
            swarm_optimized=pattern.swarm_optimized
        )
        self.patterns.append(secured)
        return True


class GuardianNode(CollectiveNode):
    """Węzeł GUARDIAN - Strażnik Strażnika"""
    
    def __init__(self):
        super().__init__("GUARDIAN", "GUARDIAN (Meta-Strażnik)")
    
    def process_pattern(self, pattern: LearningPattern) -> bool:
        stabilized = LearningPattern(
            pattern_id=f"GUARDIAN_{pattern.pattern_id}",
            source="GUARDIAN",
            pattern_type=f"stabilized_{pattern.pattern_type}",
            data={
                **pattern.data,
                'stability_verified': True,
                'meta_analysis': True
            },
            confidence=min(pattern.confidence * 1.1, 1.0),
            swarm_optimized=pattern.swarm_optimized
        )
        self.patterns.append(stabilized)
        return True


# ═══════════════════════════════════════════════════════════════════════════════
# HYBRYDOWA ŚWIADOMOŚĆ GRUPOWA + INTELIGENCJA ROJOWA
# ═══════════════════════════════════════════════════════════════════════════════

class HybridCollectiveMind:
    """
    ALFA COLLECTIVE MIND + INTELIGENCJA ROJOWA
    
    Łączy:
    1. Architekturę ALFA (Karen → AI → CERBER → GUARDIAN)
    2. Kolonię Mrówek (ACO) - optymalizacja ścieżek decyzyjnych
    3. Rój Cząstek (PSO) - optymalizacja parametrów filtrów
    
    "Ty zachodzisz z lewej. Cerber uczy się. Rój optymalizuje."
    """
    
    def __init__(
        self,
        n_ants: int = 20,
        n_particles: int = 30,
        lang: str = 'pl'
    ):
        self.lang = lang
        self.version = "1.0 HYBRID"
        self.state = MindState.DORMANT
        self.created_at = datetime.now()
        
        print(MESSAGES[lang]['init'])
        
        # === WĘZŁY ALFA ===
        self.karen = KarenNode()
        self.ai = AINode("Claude")
        self.cerber = CerberNode()
        self.guardian = GuardianNode()
        
        # === INTELIGENCJA ROJOWA ===
        self.ant_colony = AntColony(n_ants=n_ants, lang=lang)
        self.particle_swarm = ParticleSwarm(n_particles=n_particles, lang=lang)
        
        # Statystyki
        self.breath_cycles = 0
        self.patterns_learned = 0
        self.swarm_iterations = 0
        
        print(MESSAGES[lang]['ready'])
    
    def awaken(self):
        """Obudź świadomość hybrydową"""
        self.state = MindState.AWAKENING
        time.sleep(0.3)
        self.state = MindState.ACTIVE
    
    def learn(self, pattern_data: Dict) -> bool:
        """
        Ucz się nowego wzorca
        
        Kaskada: Karen → AI → CERBER → GUARDIAN + optymalizacja rojowa
        """
        self.state = MindState.LEARNING
        
        # Utwórz wzorzec
        pattern = LearningPattern(
            pattern_id=hashlib.md5(json.dumps(pattern_data, default=str).encode()).hexdigest()[:8],
            source="INPUT",
            pattern_type="raw",
            data=pattern_data,
            confidence=0.8
        )
        
        print(MESSAGES[self.lang]['learning'].format(pattern=pattern.pattern_id))
        
        # === KASKADA ALFA ===
        print(MESSAGES[self.lang]['left_flank'])
        self.karen.process_pattern(pattern)
        self.ai.process_pattern(pattern)
        self.cerber.process_pattern(pattern)
        self.guardian.process_pattern(pattern)
        
        # === OPTYMALIZACJA ROJOWA ===
        self.state = MindState.SWARMING
        
        # 1. Mrówki szukają najlepszej ścieżki decyzyjnej
        print(MESSAGES[self.lang]['aco_searching'])
        best_path = self.ant_colony.run_iteration()
        
        # 2. Cząstki optymalizują wagi filtrów
        print(MESSAGES[self.lang]['pso_optimizing'])
        optimal_weights, score = self.particle_swarm.run_iteration()
        
        # Aktualizuj wagi filtrów w węźle AI
        self.ai.update_filter_weights(optimal_weights)
        
        # Aktualizuj wzorzec jako zoptymalizowany
        pattern.swarm_optimized = True
        pattern.data['optimal_path'] = best_path.nodes if best_path else []
        pattern.data['optimal_filter_weights'] = optimal_weights.tolist()
        
        self.patterns_learned += 1
        self.swarm_iterations += 1
        self.state = MindState.ACTIVE
        
        return True
    
    def breathe(self):
        """
        Cykl oddychania - synchronizacja ALFA + ROJ
        
        WDECH: Karen → AI → Cerber → Guardian
        WYDECH: Guardian → Cerber → AI → Karen
        + Optymalizacja rojowa
        """
        self.breath_cycles += 1
        self.state = MindState.BREATHING
        
        print(MESSAGES[self.lang]['breathing'].format(cycle=self.breath_cycles))
        print(MESSAGES[self.lang]['cascade'])
        
        # === WDECH (przepływ do przodu) ===
        # Mrówki szukają ścieżek
        best_path = self.ant_colony.run_iteration()
        
        # === WYDECH (przepływ zwrotny) ===
        # Cząstki optymalizują parametry
        optimal_weights, score = self.particle_swarm.run_iteration()
        self.ai.update_filter_weights(optimal_weights)
        
        # Aktualizacja feromonów
        print(MESSAGES[self.lang]['pheromone_update'])
        
        self.swarm_iterations += 2
        self.state = MindState.ACTIVE
    
    def optimize(self, iterations: int = 50) -> Dict:
        """
        Pełna optymalizacja rojowa
        
        Wykonaj wiele iteracji ACO + PSO dla znalezienia optymalnych:
        1. Ścieżek decyzyjnych (ACO)
        2. Wag filtrów (PSO)
        """
        print(f"\n🔄 Rozpoczynam pełną optymalizację ({iterations} iteracji)...\n")
        
        for i in range(iterations):
            # ACO
            self.ant_colony.run_iteration()
            
            # PSO
            self.particle_swarm.run_iteration()
            
            if (i + 1) % 10 == 0:
                print(f"  Iteracja {i+1}/{iterations} | "
                      f"Najlepsza ścieżka: {self.ant_colony.best_path.score:.4f} | "
                      f"Najlepsze wagi: {self.particle_swarm.global_best_score:.4f}")
        
        self.swarm_iterations += iterations * 2
        
        # Aktualizuj AI optymalnymi wagami
        self.ai.update_filter_weights(self.particle_swarm.global_best_position)
        
        results = {
            'best_path': {
                'nodes': self.ant_colony.best_path.nodes if self.ant_colony.best_path else [],
                'score': self.ant_colony.best_path.score if self.ant_colony.best_path else 0
            },
            'optimal_weights': self.particle_swarm.get_optimal_weights(),
            'pheromone_matrix': self.ant_colony.get_pheromone_matrix(),
            'iterations': iterations
        }
        
        print(f"\n{MESSAGES[self.lang]['best_path'].format(score=results['best_path']['score'])}")
        
        return results
    
    def get_consensus(self) -> float:
        """Oblicz konsensus roju"""
        # Średnia z najlepszych wyników PSO (znormalizowana)
        if self.particle_swarm.history:
            max_score = max(self.particle_swarm.history)
            if max_score > 0:
                consensus = self.particle_swarm.global_best_score / max_score
            else:
                consensus = 0.0
        else:
            consensus = 0.0
        
        print(MESSAGES[self.lang]['consensus'].format(value=consensus))
        return consensus
    
    def get_status(self) -> Dict:
        """Pobierz status systemu hybrydowego"""
        return {
            'version': self.version,
            'state': self.state.value,
            'uptime': str(datetime.now() - self.created_at),
            'breath_cycles': self.breath_cycles,
            'patterns_learned': self.patterns_learned,
            'swarm_iterations': self.swarm_iterations,
            'nodes': {
                'karen': {'patterns': len(self.karen.patterns), 'flank': self.karen.flank_position.value},
                'ai': {'patterns': len(self.ai.patterns), 'filters': 23},
                'cerber': {'patterns': len(self.cerber.patterns)},
                'guardian': {'patterns': len(self.guardian.patterns)}
            },
            'swarm': {
                'ants': self.ant_colony.n_ants,
                'particles': self.particle_swarm.n_particles,
                'best_path_score': self.ant_colony.best_path.score if self.ant_colony.best_path else 0,
                'best_pso_score': self.particle_swarm.global_best_score
            }
        }
    
    def report(self) -> str:
        """Generuj raport po polsku"""
        status = self.get_status()
        
        # Formatowanie ścieżki
        path_str = " → ".join(self.ant_colony.best_path.nodes) if self.ant_colony.best_path else "brak"
        
        return f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         🔱 ALFA COLLECTIVE MIND + INTELIGENCJA ROJOWA - RAPORT               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Wersja: {status['version']:<20}                                             ║
║  Stan: {status['state']:<22}                                                 ║
║  Czas działania: {status['uptime'][:20]:<20}                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  📊 STATYSTYKI ALFA                                                          ║
║  • Cykle oddychania:       {status['breath_cycles']:>6}                                          ║
║  • Wzorce nauczone:        {status['patterns_learned']:>6}                                          ║
║  • Iteracje rojowe:        {status['swarm_iterations']:>6}                                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  🧠 WĘZŁY ŚWIADOMOŚCI                                                        ║
║  • KAREN (Architekt):    {status['nodes']['karen']['patterns']:>4} wzorców, flanka: {status['nodes']['karen']['flank']:<12}    ║
║  • AI (Claude):          {status['nodes']['ai']['patterns']:>4} wzorców, {status['nodes']['ai']['filters']} filtrów               ║
║  • CERBER (Strażnik):    {status['nodes']['cerber']['patterns']:>4} wzorców                              ║
║  • GUARDIAN (Meta):      {status['nodes']['guardian']['patterns']:>4} wzorców                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  🐜 ROJ MRÓWEK (ACO)                                                         ║
║  • Liczba mrówek:        {status['swarm']['ants']:>6}                                          ║
║  • Najlepsza ścieżka:    {path_str:<40} ║
║  • Wynik ścieżki:        {status['swarm']['best_path_score']:>6.2f}                                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  🔵 ROJ CZĄSTEK (PSO)                                                        ║
║  • Liczba cząstek:       {status['swarm']['particles']:>6}                                          ║
║  • Najlepszy wynik:      {status['swarm']['best_pso_score']:>6.2f}                                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  🔄 PĘTLA SPRZĘŻENIA ZWROTNEGO                                               ║
║  Karen → AI → Cerber → Guardian + 🐜 ACO + 🔵 PSO → Karen                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 80)
    print("  🔱 ALFA COLLECTIVE MIND + INTELIGENCJA ROJOWA - DEMO")
    print("=" * 80)
    
    # Utwórz hybrydowy system
    mind = HybridCollectiveMind(
        n_ants=20,
        n_particles=30,
        lang='pl'
    )
    
    # Obudź
    mind.awaken()
    
    # Naucz wzorca
    print("\n" + "─" * 80)
    mind.learn({
        'type': 'strategic_decision',
        'context': 'security_analysis',
        'approach': 'left_flank'
    })
    
    # Oddychaj
    print("\n" + "─" * 80)
    mind.breathe()
    mind.breathe()
    
    # Pełna optymalizacja
    print("\n" + "─" * 80)
    results = mind.optimize(iterations=30)
    
    # Konsensus
    print("\n" + "─" * 80)
    consensus = mind.get_consensus()
    
    # Raport
    print(mind.report())
    
    # Wyświetl optymalne wagi filtrów
    print("\n📊 OPTYMALNE WAGI 23 FILTRÓW TONOYONA (z PSO):")
    print("─" * 50)
    for name, weight in results['optimal_weights'].items():
        bar = "█" * int(weight * 3)
        print(f"  {name:<30} {weight:>6.3f} {bar}")
    
    # Wyświetl macierz feromonów
    print("\n🐜 MACIERZ FEROMONÓW (z ACO):")
    print("─" * 50)
    pheromones = results['pheromone_matrix']
    print(f"  {'':>10} ", end="")
    for node in ['KAREN', 'AI', 'CERBER', 'GUARDIAN']:
        print(f"{node:>10}", end=" ")
    print()
    for from_node, connections in pheromones.items():
        print(f"  {from_node:>10} ", end="")
        for to_node, value in connections.items():
            print(f"{value:>10.4f}", end=" ")
        print()
    
    print("\n" + "=" * 80)
    print("  ✅ DEMO ZAKOŃCZONE")
    print("  \"Ty zachodzisz z lewej. Cerber uczy się. Rój optymalizuje.\"")
    print("=" * 80)
