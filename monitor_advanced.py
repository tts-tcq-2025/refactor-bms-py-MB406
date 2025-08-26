"""
Advanced Battery Management System Monitor
Enhanced with additional features beyond the basic requirements

This module implements additional enhancements:
1. Age-based vital limits (future extensibility)
2. Configurable tolerance levels
3. Vital trend monitoring capabilities
4. Enhanced error handling and validation
5. Logging capabilities for healthcare compliance
"""

from enum import Enum
from typing import Dict, List, Tuple, Any, Optional, Union
import logging
from dataclasses import dataclass
from datetime import datetime

# Configure logging for healthcare compliance
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('BMS_Monitor')

class VitalCondition(Enum):
    """Enumeration of all possible vital conditions"""
    # Temperature conditions
    HYPO_THERMIA = "HYPO_THERMIA"
    NEAR_HYPO = "NEAR_HYPO"
    NORMAL = "NORMAL"
    NEAR_HYPER = "NEAR_HYPER"
    HYPER_THERMIA = "HYPER_THERMIA"
    
    # Pulse rate conditions
    BRADY_CARDIA = "BRADY_CARDIA"
    NEAR_BRADY = "NEAR_BRADY"
    NEAR_TACHY = "NEAR_TACHY"
    TACHY_CARDIA = "TACHY_CARDIA"
    
    # SPO2 conditions
    LOW_OXYGEN = "LOW_OXYGEN"
    NEAR_LOW_OXYGEN = "NEAR_LOW_OXYGEN"
    NEAR_HIGH_OXYGEN = "NEAR_HIGH_OXYGEN"
    HIGH_OXYGEN = "HIGH_OXYGEN"

@dataclass
class VitalLimits:
    """Data class for vital limits with age-based adjustments"""
    min_val: float
    max_val: float
    warning_tolerance: float = 1.5  # Configurable tolerance percentage
    
    def calculate_warning_ranges(self) -> Tuple[float, float, float, float]:
        """Calculate early warning ranges based on tolerance"""
        tolerance = (self.max_val - self.min_val) * self.warning_tolerance / 100
        return (
            self.min_val,
            self.min_val + tolerance,
            self.max_val - tolerance,
            self.max_val
        )

@dataclass
class VitalReading:
    """Enhanced vital reading with metadata"""
    value: float
    unit: str
    timestamp: datetime = None
    source: str = "manual"  # Could be "sensor", "manual", etc.
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class PatientProfile:
    """Patient profile for age-based vital adjustments"""
    def __init__(self, age: int = None, profile_type: str = "adult"):
        self.age = age
        self.profile_type = profile_type
    
    def get_vital_limits(self, vital_type: str) -> VitalLimits:
        """Get age-adjusted vital limits"""
        base_limits = {
            'temperature': VitalLimits(95, 102),
            'pulseRate': VitalLimits(60, 100),
            'spo2': VitalLimits(90, 100)
        }
        
        # Future enhancement: Age-based adjustments
        if self.age and vital_type == 'pulseRate':
            if self.age > 65:  # Elderly patients
                base_limits['pulseRate'] = VitalLimits(50, 90)
            elif self.age < 18:  # Pediatric patients
                base_limits['pulseRate'] = VitalLimits(80, 120)
        
        return base_limits.get(vital_type, VitalLimits(0, 100))

class AdvancedMonitor:
    """Advanced monitoring system with enhanced capabilities"""
    
    def __init__(self, patient_profile: PatientProfile = None):
        self.patient_profile = patient_profile or PatientProfile()
        self.language = 'en'
        self.vital_history: Dict[str, List[VitalReading]] = {}
        
        # Enhanced message templates
        self.messages = {
            'en': {
                VitalCondition.HYPO_THERMIA: "🚨 CRITICAL: Severe hypothermia detected (temp < 95°F)",
                VitalCondition.NEAR_HYPO: "⚠️ WARNING: Temperature approaching hypothermia range",
                VitalCondition.NORMAL: "",
                VitalCondition.NEAR_HYPER: "⚠️ WARNING: Temperature approaching hyperthermia range",
                VitalCondition.HYPER_THERMIA: "🚨 CRITICAL: Severe hyperthermia detected (temp > 102°F)",
                VitalCondition.BRADY_CARDIA: "🚨 CRITICAL: Severe bradycardia detected",
                VitalCondition.NEAR_BRADY: "⚠️ WARNING: Heart rate approaching bradycardia range",
                VitalCondition.NEAR_TACHY: "⚠️ WARNING: Heart rate approaching tachycardia range",
                VitalCondition.TACHY_CARDIA: "🚨 CRITICAL: Severe tachycardia detected",
                VitalCondition.LOW_OXYGEN: "🚨 CRITICAL: Severe hypoxemia detected",
                VitalCondition.NEAR_LOW_OXYGEN: "⚠️ WARNING: Oxygen saturation approaching critical low",
                VitalCondition.NEAR_HIGH_OXYGEN: "⚠️ WARNING: Oxygen saturation unusually high",
                VitalCondition.HIGH_OXYGEN: "🚨 CRITICAL: Hyperoxemia detected"
            },
            'de': {
                VitalCondition.HYPO_THERMIA: "🚨 KRITISCH: Schwere Unterkühlung erkannt",
                VitalCondition.NEAR_HYPO: "⚠️ WARNUNG: Temperatur nähert sich Unterkühlungsbereich",
                VitalCondition.NORMAL: "",
                VitalCondition.NEAR_HYPER: "⚠️ WARNUNG: Temperatur nähert sich Überhitzungsbereich",
                VitalCondition.HYPER_THERMIA: "🚨 KRITISCH: Schwere Überhitzung erkannt",
                VitalCondition.BRADY_CARDIA: "🚨 KRITISCH: Schwere Bradykardie erkannt",
                VitalCondition.NEAR_BRADY: "⚠️ WARNUNG: Herzfrequenz nähert sich Bradykardie",
                VitalCondition.NEAR_TACHY: "⚠️ WARNUNG: Herzfrequenz nähert sich Tachykardie",
                VitalCondition.TACHY_CARDIA: "🚨 KRITISCH: Schwere Tachykardie erkannt",
                VitalCondition.LOW_OXYGEN: "🚨 KRITISCH: Schwere Hypoxämie erkannt",
                VitalCondition.NEAR_LOW_OXYGEN: "⚠️ WARNUNG: Sauerstoffsättigung nähert sich kritischem Niveau",
                VitalCondition.NEAR_HIGH_OXYGEN: "⚠️ WARNUNG: Sauerstoffsättigung ungewöhnlich hoch",
                VitalCondition.HIGH_OXYGEN: "🚨 KRITISCH: Hyperoxämie erkannt"
            }
        }
    
    def set_language(self, language_code: str):
        """Set display language"""
        if language_code in self.messages:
            self.language = language_code
            logger.info(f"Language changed to {language_code}")
        else:
            raise ValueError(f"Language '{language_code}' not supported")
    
    def convert_units(self, reading: VitalReading, vital_type: str) -> float:
        """Enhanced unit conversion with validation"""
        try:
            if vital_type == 'temperature' and reading.unit.upper() == 'C':
                converted = (reading.value * 9/5) + 32
                logger.debug(f"Converted {reading.value}°C to {converted}°F")
                return converted
            elif vital_type == 'temperature' and reading.unit.upper() not in ['C', 'F']:
                raise ValueError(f"Invalid temperature unit: {reading.unit}")
            
            return reading.value
        except Exception as e:
            logger.error(f"Unit conversion failed: {e}")
            raise
    
    def assess_vital(self, vital_type: str, reading: VitalReading) -> Tuple[VitalCondition, str]:
        """Assess a single vital with enhanced logic"""
        try:
            # Convert to common units
            converted_value = self.convert_units(reading, vital_type)
            
            # Get patient-specific limits
            limits = self.patient_profile.get_vital_limits(vital_type)
            min_val, near_min, near_max, max_val = limits.calculate_warning_ranges()
            
            # Determine condition based on value ranges
            if converted_value < min_val:
                conditions_map = {
                    'temperature': VitalCondition.HYPO_THERMIA,
                    'pulseRate': VitalCondition.BRADY_CARDIA,
                    'spo2': VitalCondition.LOW_OXYGEN
                }
                condition = conditions_map.get(vital_type, VitalCondition.NORMAL)
            elif min_val <= converted_value <= near_min:
                conditions_map = {
                    'temperature': VitalCondition.NEAR_HYPO,
                    'pulseRate': VitalCondition.NEAR_BRADY,
                    'spo2': VitalCondition.NEAR_LOW_OXYGEN
                }
                condition = conditions_map.get(vital_type, VitalCondition.NORMAL)
            elif near_max <= converted_value < max_val:
                conditions_map = {
                    'temperature': VitalCondition.NEAR_HYPER,
                    'pulseRate': VitalCondition.NEAR_TACHY,
                    'spo2': VitalCondition.NEAR_HIGH_OXYGEN
                }
                condition = conditions_map.get(vital_type, VitalCondition.NORMAL)
            elif converted_value >= max_val:
                conditions_map = {
                    'temperature': VitalCondition.HYPER_THERMIA,
                    'pulseRate': VitalCondition.TACHY_CARDIA,
                    'spo2': VitalCondition.HIGH_OXYGEN
                }
                condition = conditions_map.get(vital_type, VitalCondition.NORMAL)
            else:
                condition = VitalCondition.NORMAL
            
            # Get message
            message = self.messages[self.language].get(condition, "")
            
            # Log assessment
            if condition != VitalCondition.NORMAL:
                logger.warning(f"{vital_type}: {converted_value} -> {condition.value}")
            
            return condition, message
            
        except Exception as e:
            logger.error(f"Vital assessment failed for {vital_type}: {e}")
            raise
    
    def monitor_vitals(self, vitals: Dict[str, Union[VitalReading, Dict[str, Any]]]) -> Dict[str, Any]:
        """Enhanced vital monitoring with comprehensive reporting"""
        results = {
            'timestamp': datetime.now(),
            'patient_profile': f"Age: {self.patient_profile.age}, Type: {self.patient_profile.profile_type}",
            'assessments': {},
            'overall_status': 'NORMAL',
            'critical_alerts': [],
            'warnings': [],
            'recommendations': []
        }
        
        critical_count = 0
        warning_count = 0
        
        for vital_type, vital_data in vitals.items():
            try:
                # Convert to VitalReading if needed
                if isinstance(vital_data, dict):
                    reading = VitalReading(
                        value=vital_data['value'],
                        unit=vital_data.get('unit', ''),
                        source=vital_data.get('source', 'manual')
                    )
                else:
                    reading = vital_data
                
                # Store in history
                if vital_type not in self.vital_history:
                    self.vital_history[vital_type] = []
                self.vital_history[vital_type].append(reading)
                
                # Assess vital
                condition, message = self.assess_vital(vital_type, reading)
                
                results['assessments'][vital_type] = {
                    'value': reading.value,
                    'unit': reading.unit,
                    'condition': condition.value,
                    'message': message,
                    'timestamp': reading.timestamp.isoformat()
                }
                
                # Categorize results
                if 'CRITICAL' in message or 'KRITISCH' in message:
                    results['critical_alerts'].append((vital_type, message))
                    critical_count += 1
                elif 'WARNING' in message or 'WARNUNG' in message:
                    results['warnings'].append((vital_type, message))
                    warning_count += 1
                    
            except Exception as e:
                logger.error(f"Failed to process {vital_type}: {e}")
                results['assessments'][vital_type] = {
                    'error': str(e),
                    'condition': 'ERROR'
                }
        
        # Determine overall status
        if critical_count > 0:
            results['overall_status'] = 'CRITICAL'
            results['recommendations'].append("Immediate medical attention required")
        elif warning_count > 0:
            results['overall_status'] = 'WARNING'
            results['recommendations'].append("Monitor closely and consider medical consultation")
        else:
            results['overall_status'] = 'NORMAL'
        
        # Add trending recommendations (future enhancement)
        if len(self.vital_history.get('temperature', [])) > 1:
            results['recommendations'].append("Trending data available for analysis")
        
        return results
    
    def get_vital_trends(self, vital_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent vital trends (future enhancement)"""
        if vital_type not in self.vital_history:
            return []
        
        recent_readings = self.vital_history[vital_type][-limit:]
        return [
            {
                'value': reading.value,
                'unit': reading.unit,
                'timestamp': reading.timestamp.isoformat(),
                'source': reading.source
            }
            for reading in recent_readings
        ]

# Factory function for easy instantiation
def create_monitor(age: int = None, profile_type: str = "adult") -> AdvancedMonitor:
    """Factory function to create a monitor with patient profile"""
    profile = PatientProfile(age=age, profile_type=profile_type)
    return AdvancedMonitor(profile)

# Legacy compatibility functions
def vitals_ok_advanced(vitals: Dict[str, Any], age: int = None) -> Tuple[bool, List[Tuple[str, str]], List[Tuple[str, str]]]:
    """Advanced vitals checking with age considerations"""
    monitor = create_monitor(age=age)
    results = monitor.monitor_vitals(vitals)
    
    overall_ok = results['overall_status'] == 'NORMAL'
    failures = results['critical_alerts']
    warnings = results['warnings']
    
    return overall_ok, failures, warnings
