"""
GUARDIAN - CERBER LIFE MONITOR & ADAPTIVE CODE ENGINE
======================================================
Meta-Security System with Self-Evolving Intelligence
Author: Karen Tonoyan
Version: 1.0
License: CC BY-SA 4.0

"Guardian nie śpi nigdy. Guardian czuwa nad tym, który czuwa."
"Guardian never sleeps. Guardian watches over the one who watches."
"""

import hashlib
import time
import json
import threading
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
import copy
import random


# ============================================================================
# MULTILINGUAL MESSAGES / WIELOJĘZYCZNE KOMUNIKATY
# ============================================================================

MESSAGES = {
    'pl': {
        'heartbeat_ok': "💓 CERBER żyje - puls: {pulse}ms",
        'heartbeat_fail': "💀 CERBER NIE ODPOWIADA - ostatni puls: {last}",
        'health_ok': "✅ Stan zdrowia CERBER: OPTYMALNY",
        'health_warn': "⚠️ Stan zdrowia CERBER: OSTRZEŻENIE - {issue}",
        'health_critical': "🚨 Stan zdrowia CERBER: KRYTYCZNY - {issue}",
        'integrity_ok': "🔐 Integralność kodu: ZWERYFIKOWANA",
        'integrity_fail': "🔓 NARUSZENIE INTEGRALNOŚCI: {component}",
        'healing_start': "🔧 Rozpoczynam samoleczenie: {component}",
        'healing_complete': "✅ Samoleczenie zakończone: {component}",
        'code_evolving': "🧬 Kod ewoluuje w odpowiedzi na: {threat}",
        'guardian_active': "🛡️ GUARDIAN AKTYWNY - Monitoruję {count} instancji CERBER",
    },
    'en': {
        'heartbeat_ok': "💓 CERBER alive - pulse: {pulse}ms",
        'heartbeat_fail': "💀 CERBER NOT RESPONDING - last pulse: {last}",
        'health_ok': "✅ CERBER health status: OPTIMAL",
        'health_warn': "⚠️ CERBER health status: WARNING - {issue}",
        'health_critical': "🚨 CERBER health status: CRITICAL - {issue}",
        'integrity_ok': "🔐 Code integrity: VERIFIED",
        'integrity_fail': "🔓 INTEGRITY BREACH: {component}",
        'healing_start': "🔧 Starting self-healing: {component}",
        'healing_complete': "✅ Self-healing complete: {component}",
        'code_evolving': "🧬 Code evolving in response to: {threat}",
        'guardian_active': "🛡️ GUARDIAN ACTIVE - Monitoring {count} CERBER instances",
    },
    'ru': {
        'heartbeat_ok': "💓 CERBER жив - пульс: {pulse}мс",
        'heartbeat_fail': "💀 CERBER НЕ ОТВЕЧАЕТ - последний пульс: {last}",
        'health_ok': "✅ Состояние CERBER: ОПТИМАЛЬНОЕ",
        'health_warn': "⚠️ Состояние CERBER: ПРЕДУПРЕЖДЕНИЕ - {issue}",
        'health_critical': "🚨 Состояние CERBER: КРИТИЧЕСКОЕ - {issue}",
        'integrity_ok': "🔐 Целостность кода: ПРОВЕРЕНА",
        'integrity_fail': "🔓 НАРУШЕНИЕ ЦЕЛОСТНОСТИ: {component}",
        'healing_start': "🔧 Начинаю самоисцеление: {component}",
        'healing_complete': "✅ Самоисцеление завершено: {component}",
        'code_evolving': "🧬 Код эволюционирует в ответ на: {threat}",
        'guardian_active': "🛡️ GUARDIAN АКТИВЕН - Мониторю {count} экземпляров CERBER",
    },
    'de': {
        'heartbeat_ok': "💓 CERBER lebt - Puls: {pulse}ms",
        'heartbeat_fail': "💀 CERBER ANTWORTET NICHT - letzter Puls: {last}",
        'health_ok': "✅ CERBER Gesundheit: OPTIMAL",
        'health_warn': "⚠️ CERBER Gesundheit: WARNUNG - {issue}",
        'health_critical': "🚨 CERBER Gesundheit: KRITISCH - {issue}",
        'integrity_ok': "🔐 Code-Integrität: VERIFIZIERT",
        'integrity_fail': "🔓 INTEGRITÄTSVERLETZUNG: {component}",
        'healing_start': "🔧 Starte Selbstheilung: {component}",
        'healing_complete': "✅ Selbstheilung abgeschlossen: {component}",
        'code_evolving': "🧬 Code evolviert als Reaktion auf: {threat}",
        'guardian_active': "🛡️ GUARDIAN AKTIV - Überwache {count} CERBER-Instanzen",
    },
    'hy': {
        'heartbeat_ok': "💓 CERBER ապdelays - delays: {pulse}ms",
        'heartbeat_fail': "💀 CERBER ՉԻ Պdelays - delays delays: {last}",
        'health_ok': "✅ CERBER delays: Օdelays",
        'guardian_active': "🛡️ GUARDIAN DELAYS - delays {count} CERBER",
    }
}


# ============================================================================
# CERBER STATE ENUMS
# ============================================================================

class CerberState(Enum):
    """Stan cyklu życia CERBERA / CERBER lifecycle state"""
    INIT = "INIT"           # Inicjalizacja
    READY = "READY"         # Gotowy do działania
    ACTIVE = "ACTIVE"       # Aktywny
    PATROL = "PATROL"       # Patrolowanie
    ALERT = "ALERT"         # Stan alertu
    THREAT = "THREAT"       # Wykryto zagrożenie
    RECOVERY = "RECOVERY"   # Odzyskiwanie
    DORMANT = "DORMANT"     # Uśpiony
    DEAD = "DEAD"           # Martwy (wymaga restartu)


class HealthStatus(Enum):
    """Status zdrowia / Health status"""
    OPTIMAL = "OPTIMAL"
    GOOD = "GOOD"
    DEGRADED = "DEGRADED"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    DEAD = "DEAD"


class ThreatType(Enum):
    """Typy zagrożeń / Threat types"""
    NONE = "NONE"
    INTRUSION = "INTRUSION"
    CORRUPTION = "CORRUPTION"
    HALLUCINATION = "HALLUCINATION"
    MANIPULATION = "MANIPULATION"
    OVERLOAD = "OVERLOAD"
    INJECTION = "INJECTION"


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Heartbeat:
    """Struktura pulsu CERBERA / CERBER heartbeat structure"""
    timestamp: datetime
    pulse_ms: float
    state: CerberState
    health: HealthStatus
    memory_usage: float
    cpu_usage: float
    active_filters: int
    threats_blocked: int
    
    def is_alive(self, timeout_ms: float = 5000) -> bool:
        """Sprawdź czy CERBER żyje / Check if CERBER is alive"""
        age_ms = (datetime.now() - self.timestamp).total_seconds() * 1000
        return age_ms < timeout_ms


@dataclass
class CerberInstance:
    """Instancja CERBERA monitorowana przez GUARDIAN"""
    instance_id: str
    name: str
    state: CerberState = CerberState.INIT
    health: HealthStatus = HealthStatus.OPTIMAL
    last_heartbeat: Optional[Heartbeat] = None
    code_hash: str = ""
    version: str = "1.0"
    created_at: datetime = field(default_factory=datetime.now)
    threats_handled: int = 0
    self_heals: int = 0
    evolution_count: int = 0


@dataclass
class AdaptiveCodeBlock:
    """Blok adaptacyjnego kodu / Adaptive code block"""
    block_id: str
    name: str
    code: str
    version: int = 1
    fitness_score: float = 1.0
    mutations: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    last_mutation: Optional[datetime] = None
    
    def get_hash(self) -> str:
        """Oblicz hash kodu / Calculate code hash"""
        return hashlib.sha256(self.code.encode()).hexdigest()[:16]


# ============================================================================
# ADAPTIVE CODE ENGINE - SILNIK ADAPTACYJNEGO KODU
# ============================================================================

class AdaptiveCodeEngine:
    """
    Silnik adaptacyjnego kodu - samodzielnie ewoluuje w odpowiedzi na zagrożenia
    Adaptive code engine - self-evolves in response to threats
    """
    
    def __init__(self, lang: str = 'pl'):
        self.lang = lang
        self.code_blocks: Dict[str, AdaptiveCodeBlock] = {}
        self.evolution_history: List[Dict] = []
        self.mutation_rate: float = 0.1
        self.fitness_threshold: float = 0.5
        self.logger = logging.getLogger("AdaptiveCode")
        
        # Inicjalizuj bazowe bloki kodu
        self._initialize_base_blocks()
    
    def _initialize_base_blocks(self):
        """Inicjalizuj bazowe bloki adaptacyjnego kodu"""
        
        # Blok detekcji zagrożeń
        self.code_blocks['threat_detection'] = AdaptiveCodeBlock(
            block_id="TD001",
            name="Threat Detection Algorithm",
            code='''
def detect_threat(input_data: Dict) -> Tuple[bool, ThreatType, float]:
    """Algorytm detekcji zagrożeń - wersja bazowa"""
    confidence = 0.0
    threat_type = ThreatType.NONE
    
    # Sprawdź wzorce intruzji
    if 'injection_patterns' in input_data:
        patterns = input_data['injection_patterns']
        if any(p in str(input_data) for p in patterns):
            threat_type = ThreatType.INJECTION
            confidence = 0.85
    
    # Sprawdź anomalie
    if 'anomaly_score' in input_data:
        if input_data['anomaly_score'] > 0.7:
            threat_type = ThreatType.INTRUSION
            confidence = input_data['anomaly_score']
    
    # Sprawdź halucynacje AI
    if 'hallucination_markers' in input_data:
        markers = input_data['hallucination_markers']
        if len(markers) > 3:
            threat_type = ThreatType.HALLUCINATION
            confidence = min(len(markers) * 0.2, 0.95)
    
    return confidence > 0.5, threat_type, confidence
'''
        )
        
        # Blok odpowiedzi na zagrożenia
        self.code_blocks['threat_response'] = AdaptiveCodeBlock(
            block_id="TR001",
            name="Threat Response Algorithm",
            code='''
def respond_to_threat(threat_type: ThreatType, confidence: float) -> Dict:
    """Algorytm odpowiedzi na zagrożenia - wersja bazowa"""
    response = {
        'action': 'MONITOR',
        'escalate': False,
        'block': False,
        'notify': False,
        'heal': False
    }
    
    if confidence < 0.5:
        return response
    
    if threat_type == ThreatType.INJECTION:
        response['action'] = 'BLOCK_AND_QUARANTINE'
        response['block'] = True
        response['notify'] = True
        
    elif threat_type == ThreatType.HALLUCINATION:
        response['action'] = 'VERIFY_AND_CORRECT'
        response['heal'] = True
        
    elif threat_type == ThreatType.INTRUSION:
        response['action'] = 'ISOLATE_AND_ANALYZE'
        response['block'] = True
        response['escalate'] = True
        
    elif threat_type == ThreatType.MANIPULATION:
        response['action'] = 'RESET_AND_VERIFY'
        response['heal'] = True
        response['notify'] = True
    
    if confidence > 0.9:
        response['escalate'] = True
    
    return response
'''
        )
        
        # Blok samoleczenia
        self.code_blocks['self_healing'] = AdaptiveCodeBlock(
            block_id="SH001",
            name="Self-Healing Algorithm",
            code='''
def self_heal(component: str, damage_type: str, severity: float) -> bool:
    """Algorytm samoleczenia - wersja bazowa"""
    healing_strategies = {
        'corruption': ['restore_backup', 'regenerate', 'rebuild'],
        'overload': ['throttle', 'shed_load', 'restart'],
        'injection': ['sanitize', 'quarantine', 'purge'],
        'hallucination': ['verify', 'correct', 'retrain']
    }
    
    if damage_type not in healing_strategies:
        return False
    
    strategies = healing_strategies[damage_type]
    
    # Wybierz strategię na podstawie severity
    if severity < 0.3:
        strategy = strategies[0]  # Łagodna
    elif severity < 0.7:
        strategy = strategies[1]  # Średnia
    else:
        strategy = strategies[2]  # Agresywna
    
    # Wykonaj leczenie
    success = execute_healing_strategy(component, strategy)
    
    return success
'''
        )
    
    def evolve_block(self, block_id: str, threat_data: Dict) -> bool:
        """
        Ewoluuj blok kodu w odpowiedzi na zagrożenie
        Evolve code block in response to threat
        """
        if block_id not in self.code_blocks:
            return False
        
        block = self.code_blocks[block_id]
        
        # Oceń fitness obecnego kodu
        current_fitness = self._evaluate_fitness(block, threat_data)
        
        if current_fitness < self.fitness_threshold:
            # Mutuj kod
            mutated_code = self._mutate_code(block.code, threat_data)
            
            # Testuj mutację
            test_block = AdaptiveCodeBlock(
                block_id=f"{block_id}_test",
                name=f"{block.name} (mutated)",
                code=mutated_code,
                version=block.version + 1
            )
            
            new_fitness = self._evaluate_fitness(test_block, threat_data)
            
            if new_fitness > current_fitness:
                # Akceptuj mutację
                block.code = mutated_code
                block.version += 1
                block.mutations += 1
                block.fitness_score = new_fitness
                block.last_mutation = datetime.now()
                
                self.evolution_history.append({
                    'block_id': block_id,
                    'timestamp': datetime.now().isoformat(),
                    'old_fitness': current_fitness,
                    'new_fitness': new_fitness,
                    'threat_type': threat_data.get('type', 'unknown')
                })
                
                self.logger.info(f"🧬 {MESSAGES[self.lang]['code_evolving'].format(threat=threat_data.get('type', 'unknown'))}")
                return True
        
        return False
    
    def _evaluate_fitness(self, block: AdaptiveCodeBlock, threat_data: Dict) -> float:
        """Oceń fitness bloku kodu / Evaluate code block fitness"""
        # Symulowana ocena fitness
        base_fitness = block.fitness_score
        
        # Bonusy za dopasowanie do zagrożenia
        threat_type = threat_data.get('type', '')
        if threat_type in block.code:
            base_fitness += 0.1
        
        # Kary za złożoność
        code_length = len(block.code)
        if code_length > 2000:
            base_fitness -= 0.05
        
        # Bonus za wersję
        base_fitness += block.version * 0.01
        
        return min(max(base_fitness, 0.0), 1.0)
    
    def _mutate_code(self, code: str, threat_data: Dict) -> str:
        """Mutuj kod / Mutate code"""
        mutated = code
        
        threat_type = threat_data.get('type', '')
        
        # Dodaj nowe wzorce detekcji
        if threat_type and threat_type not in code:
            insertion = f'''
    # [EVOLVED] Nowy wzorzec dla: {threat_type}
    if '{threat_type.lower()}' in str(input_data).lower():
        confidence += 0.15
'''
            # Wstaw przed return
            if 'return' in mutated:
                mutated = mutated.replace('    return', insertion + '    return', 1)
        
        # Dostosuj progi
        if random.random() < self.mutation_rate:
            mutated = mutated.replace('0.7', str(round(random.uniform(0.6, 0.8), 2)))
            mutated = mutated.replace('0.85', str(round(random.uniform(0.8, 0.95), 2)))
        
        return mutated
    
    def get_code_hash(self) -> str:
        """Oblicz hash wszystkich bloków kodu"""
        all_code = "".join(b.code for b in self.code_blocks.values())
        return hashlib.sha256(all_code.encode()).hexdigest()


# ============================================================================
# LIFECYCLE MONITOR - MONITOR CYKLU ŻYCIA
# ============================================================================

class LifecycleMonitor:
    """
    Monitor cyklu życia CERBERA
    CERBER lifecycle monitor
    """
    
    def __init__(self, lang: str = 'pl'):
        self.lang = lang
        self.instances: Dict[str, CerberInstance] = {}
        self.heartbeat_interval_ms: float = 100  # 100ms
        self.timeout_ms: float = 5000  # 5 sekund
        self.monitoring: bool = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.logger = logging.getLogger("LifecycleMonitor")
        
        # Callbacks
        self.on_death: Optional[Callable] = None
        self.on_degradation: Optional[Callable] = None
        self.on_threat: Optional[Callable] = None
    
    def register_instance(self, instance: CerberInstance):
        """Zarejestruj instancję CERBERA / Register CERBER instance"""
        self.instances[instance.instance_id] = instance
        self.logger.info(f"📝 Zarejestrowano instancję: {instance.name} ({instance.instance_id})")
    
    def unregister_instance(self, instance_id: str):
        """Wyrejestruj instancję / Unregister instance"""
        if instance_id in self.instances:
            del self.instances[instance_id]
    
    def receive_heartbeat(self, instance_id: str, heartbeat: Heartbeat):
        """Odbierz heartbeat od CERBERA / Receive heartbeat from CERBER"""
        if instance_id not in self.instances:
            self.logger.warning(f"⚠️ Heartbeat od nieznanej instancji: {instance_id}")
            return
        
        instance = self.instances[instance_id]
        instance.last_heartbeat = heartbeat
        instance.state = heartbeat.state
        instance.health = heartbeat.health
        
        # Sprawdź zdrowie
        if heartbeat.health in [HealthStatus.WARNING, HealthStatus.CRITICAL]:
            if self.on_degradation:
                self.on_degradation(instance, heartbeat)
    
    def check_instance_health(self, instance_id: str) -> Dict:
        """Sprawdź zdrowie instancji / Check instance health"""
        if instance_id not in self.instances:
            return {'status': 'UNKNOWN', 'message': 'Instance not found'}
        
        instance = self.instances[instance_id]
        
        if instance.last_heartbeat is None:
            return {
                'status': 'DEAD',
                'message': MESSAGES[self.lang]['heartbeat_fail'].format(last='NEVER')
            }
        
        if not instance.last_heartbeat.is_alive(self.timeout_ms):
            instance.state = CerberState.DEAD
            instance.health = HealthStatus.DEAD
            
            if self.on_death:
                self.on_death(instance)
            
            return {
                'status': 'DEAD',
                'message': MESSAGES[self.lang]['heartbeat_fail'].format(
                    last=instance.last_heartbeat.timestamp.isoformat()
                )
            }
        
        return {
            'status': instance.health.value,
            'message': MESSAGES[self.lang]['heartbeat_ok'].format(
                pulse=instance.last_heartbeat.pulse_ms
            ),
            'state': instance.state.value,
            'threats_blocked': instance.last_heartbeat.threats_blocked
        }
    
    def verify_integrity(self, instance_id: str, expected_hash: str) -> bool:
        """Weryfikuj integralność kodu CERBERA / Verify CERBER code integrity"""
        if instance_id not in self.instances:
            return False
        
        instance = self.instances[instance_id]
        
        if instance.code_hash == expected_hash:
            self.logger.info(MESSAGES[self.lang]['integrity_ok'])
            return True
        else:
            self.logger.error(MESSAGES[self.lang]['integrity_fail'].format(
                component=instance.name
            ))
            return False
    
    def get_all_status(self) -> Dict[str, Dict]:
        """Pobierz status wszystkich instancji / Get all instances status"""
        return {
            instance_id: self.check_instance_health(instance_id)
            for instance_id in self.instances
        }
    
    def start_monitoring(self):
        """Rozpocznij monitorowanie / Start monitoring"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info(MESSAGES[self.lang]['guardian_active'].format(
            count=len(self.instances)
        ))
    
    def stop_monitoring(self):
        """Zatrzymaj monitorowanie / Stop monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
    
    def _monitor_loop(self):
        """Pętla monitorowania / Monitoring loop"""
        while self.monitoring:
            for instance_id in list(self.instances.keys()):
                self.check_instance_health(instance_id)
            time.sleep(self.heartbeat_interval_ms / 1000)


# ============================================================================
# SELF-HEALING MODULE - MODUŁ SAMOLECZENIA
# ============================================================================

class SelfHealingModule:
    """
    Moduł samoleczenia - automatyczna naprawa uszkodzonych komponentów
    Self-healing module - automatic repair of damaged components
    """
    
    def __init__(self, lang: str = 'pl'):
        self.lang = lang
        self.backup_states: Dict[str, Dict] = {}
        self.healing_history: List[Dict] = []
        self.max_heal_attempts: int = 3
        self.logger = logging.getLogger("SelfHealing")
    
    def create_backup(self, instance_id: str, state: Dict):
        """Utwórz backup stanu / Create state backup"""
        self.backup_states[instance_id] = {
            'state': copy.deepcopy(state),
            'timestamp': datetime.now(),
            'hash': hashlib.sha256(json.dumps(state, default=str).encode()).hexdigest()
        }
    
    def heal(self, instance: CerberInstance, damage_type: str, severity: float) -> bool:
        """
        Lecz uszkodzoną instancję / Heal damaged instance
        """
        self.logger.info(MESSAGES[self.lang]['healing_start'].format(
            component=instance.name
        ))
        
        healing_success = False
        attempts = 0
        
        while not healing_success and attempts < self.max_heal_attempts:
            attempts += 1
            
            if severity < 0.3:
                # Łagodne leczenie - restart komponentu
                healing_success = self._soft_heal(instance)
            elif severity < 0.7:
                # Średnie leczenie - przywróć z backupu
                healing_success = self._restore_from_backup(instance)
            else:
                # Agresywne leczenie - pełna regeneracja
                healing_success = self._full_regeneration(instance)
            
            if not healing_success:
                severity += 0.1  # Eskaluj strategię
        
        if healing_success:
            instance.self_heals += 1
            instance.health = HealthStatus.GOOD
            instance.state = CerberState.RECOVERY
            
            self.healing_history.append({
                'instance_id': instance.instance_id,
                'timestamp': datetime.now().isoformat(),
                'damage_type': damage_type,
                'severity': severity,
                'attempts': attempts,
                'success': True
            })
            
            self.logger.info(MESSAGES[self.lang]['healing_complete'].format(
                component=instance.name
            ))
        
        return healing_success
    
    def _soft_heal(self, instance: CerberInstance) -> bool:
        """Łagodne leczenie / Soft healing"""
        # Symulacja restartu komponentu
        instance.state = CerberState.INIT
        time.sleep(0.1)  # Symulacja restartu
        instance.state = CerberState.READY
        return True
    
    def _restore_from_backup(self, instance: CerberInstance) -> bool:
        """Przywróć z backupu / Restore from backup"""
        if instance.instance_id not in self.backup_states:
            return False
        
        backup = self.backup_states[instance.instance_id]
        # Symulacja przywracania stanu
        instance.state = CerberState.RECOVERY
        time.sleep(0.2)
        instance.state = CerberState.READY
        return True
    
    def _full_regeneration(self, instance: CerberInstance) -> bool:
        """Pełna regeneracja / Full regeneration"""
        # Symulacja pełnej regeneracji
        instance.state = CerberState.INIT
        instance.health = HealthStatus.DEGRADED
        time.sleep(0.5)
        instance.state = CerberState.READY
        instance.health = HealthStatus.GOOD
        return True


# ============================================================================
# GUARDIAN CORE - GŁÓWNA KLASA GUARDIAN
# ============================================================================

class Guardian:
    """
    GUARDIAN - Meta-system bezpieczeństwa
    Strażnik strażnika z adaptacyjnym kodem i samoleczeniem
    
    Guardian of the guardian with adaptive code and self-healing
    """
    
    def __init__(self, lang: str = 'pl'):
        self.lang = lang
        self.version = "1.0"
        self.created_at = datetime.now()
        
        # Moduły
        self.lifecycle_monitor = LifecycleMonitor(lang)
        self.adaptive_code = AdaptiveCodeEngine(lang)
        self.self_healing = SelfHealingModule(lang)
        
        # Stan
        self.active = False
        self.threats_detected: int = 0
        self.evolutions_performed: int = 0
        self.heals_performed: int = 0
        
        # Logger
        self.logger = logging.getLogger("Guardian")
        
        # Konfiguracja callbacków
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        """Konfiguruj callbacki / Setup callbacks"""
        self.lifecycle_monitor.on_death = self._on_cerber_death
        self.lifecycle_monitor.on_degradation = self._on_cerber_degradation
        self.lifecycle_monitor.on_threat = self._on_cerber_threat
    
    def _on_cerber_death(self, instance: CerberInstance):
        """Handler śmierci CERBERA / CERBER death handler"""
        self.logger.critical(f"💀 CERBER DEAD: {instance.name}")
        
        # Próba reanimacji
        success = self.self_healing.heal(instance, 'death', 1.0)
        
        if not success:
            self.logger.critical(f"❌ Nie udało się reanimować: {instance.name}")
    
    def _on_cerber_degradation(self, instance: CerberInstance, heartbeat: Heartbeat):
        """Handler degradacji CERBERA / CERBER degradation handler"""
        self.logger.warning(f"⚠️ CERBER DEGRADED: {instance.name} - {heartbeat.health.value}")
        
        # Samoleczenie
        severity = 0.3 if heartbeat.health == HealthStatus.WARNING else 0.7
        self.self_healing.heal(instance, 'degradation', severity)
        self.heals_performed += 1
    
    def _on_cerber_threat(self, instance: CerberInstance, threat_data: Dict):
        """Handler zagrożenia / Threat handler"""
        self.threats_detected += 1
        
        # Ewoluuj kod w odpowiedzi na zagrożenie
        evolved = self.adaptive_code.evolve_block('threat_detection', threat_data)
        if evolved:
            self.evolutions_performed += 1
    
    def register_cerber(self, instance: CerberInstance):
        """Zarejestruj CERBERA do monitorowania / Register CERBER for monitoring"""
        self.lifecycle_monitor.register_instance(instance)
        self.self_healing.create_backup(instance.instance_id, {
            'state': instance.state.value,
            'health': instance.health.value,
            'version': instance.version
        })
    
    def start(self):
        """Uruchom GUARDIAN / Start GUARDIAN"""
        self.active = True
        self.lifecycle_monitor.start_monitoring()
        self.logger.info(f"🛡️ GUARDIAN ACTIVATED - Version {self.version}")
        self.logger.info(MESSAGES[self.lang]['guardian_active'].format(
            count=len(self.lifecycle_monitor.instances)
        ))
    
    def stop(self):
        """Zatrzymaj GUARDIAN / Stop GUARDIAN"""
        self.active = False
        self.lifecycle_monitor.stop_monitoring()
        self.logger.info("🛡️ GUARDIAN DEACTIVATED")
    
    def get_status(self) -> Dict:
        """Pobierz pełny status / Get full status"""
        return {
            'guardian': {
                'version': self.version,
                'active': self.active,
                'uptime': str(datetime.now() - self.created_at),
                'threats_detected': self.threats_detected,
                'evolutions_performed': self.evolutions_performed,
                'heals_performed': self.heals_performed,
                'code_hash': self.adaptive_code.get_code_hash()
            },
            'instances': self.lifecycle_monitor.get_all_status(),
            'adaptive_code': {
                'blocks': len(self.adaptive_code.code_blocks),
                'total_mutations': sum(b.mutations for b in self.adaptive_code.code_blocks.values()),
                'evolution_history': len(self.adaptive_code.evolution_history)
            },
            'healing': {
                'backups': len(self.self_healing.backup_states),
                'history': len(self.self_healing.healing_history)
            }
        }
    
    def report(self, lang: Optional[str] = None) -> str:
        """Generuj raport / Generate report"""
        lang = lang or self.lang
        status = self.get_status()
        
        if lang == 'pl':
            return f"""
╔══════════════════════════════════════════════════════════════════╗
║                    🛡️ GUARDIAN STATUS REPORT                     ║
╠══════════════════════════════════════════════════════════════════╣
║  Wersja: {status['guardian']['version']}                                              ║
║  Status: {'AKTYWNY 🟢' if status['guardian']['active'] else 'NIEAKTYWNY 🔴'}                                    ║
║  Czas działania: {status['guardian']['uptime'][:20]}                          ║
╠══════════════════════════════════════════════════════════════════╣
║  📊 STATYSTYKI                                                   ║
║  • Wykryte zagrożenia: {status['guardian']['threats_detected']:>6}                              ║
║  • Ewolucje kodu: {status['guardian']['evolutions_performed']:>10}                              ║
║  • Samoleczenia: {status['guardian']['heals_performed']:>11}                              ║
║  • Hash kodu: {status['guardian']['code_hash'][:16]}...                        ║
╠══════════════════════════════════════════════════════════════════╣
║  🐺 MONITOROWANE INSTANCJE CERBER: {len(status['instances']):>3}                          ║
╠══════════════════════════════════════════════════════════════════╣
║  🧬 KOD ADAPTACYJNY                                              ║
║  • Bloki kodu: {status['adaptive_code']['blocks']:>12}                              ║
║  • Mutacje: {status['adaptive_code']['total_mutations']:>16}                              ║
╚══════════════════════════════════════════════════════════════════╝
"""
        else:
            return f"""
╔══════════════════════════════════════════════════════════════════╗
║                    🛡️ GUARDIAN STATUS REPORT                     ║
╠══════════════════════════════════════════════════════════════════╣
║  Version: {status['guardian']['version']}                                             ║
║  Status: {'ACTIVE 🟢' if status['guardian']['active'] else 'INACTIVE 🔴'}                                      ║
║  Uptime: {status['guardian']['uptime'][:20]}                            ║
╠══════════════════════════════════════════════════════════════════╣
║  📊 STATISTICS                                                   ║
║  • Threats detected: {status['guardian']['threats_detected']:>6}                                ║
║  • Code evolutions: {status['guardian']['evolutions_performed']:>7}                                ║
║  • Self-heals: {status['guardian']['heals_performed']:>12}                                ║
╚══════════════════════════════════════════════════════════════════╝
"""


# ============================================================================
# MAIN - DEMO
# ============================================================================

if __name__ == "__main__":
    # Konfiguracja logowania
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    )
    
    # Utwórz GUARDIAN
    guardian = Guardian(lang='pl')
    
    # Utwórz instancję CERBER do monitorowania
    cerber = CerberInstance(
        instance_id="CERBER-001",
        name="CERBER Prime",
        state=CerberState.READY,
        health=HealthStatus.OPTIMAL,
        version="2.0"
    )
    
    # Zarejestruj CERBER
    guardian.register_cerber(cerber)
    
    # Uruchom GUARDIAN
    guardian.start()
    
    # Symuluj heartbeat
    heartbeat = Heartbeat(
        timestamp=datetime.now(),
        pulse_ms=50.0,
        state=CerberState.PATROL,
        health=HealthStatus.OPTIMAL,
        memory_usage=45.5,
        cpu_usage=23.1,
        active_filters=23,
        threats_blocked=42
    )
    
    guardian.lifecycle_monitor.receive_heartbeat("CERBER-001", heartbeat)
    
    # Wyświetl raport
    print(guardian.report('pl'))
    print(guardian.report('en'))
    
    # Zatrzymaj
    guardian.stop()
