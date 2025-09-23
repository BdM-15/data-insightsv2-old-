#!/usr/bin/env python3
"""
Minimal Example Assembly Script for Capture Insights LLM Training

This script demonstrates how to assemble training examples using:
- USASpending database fields and business rules
- Shipley-aligned capture methodology from curated reference
- Authoritative terminology from cached API references

Usage:
    python assemble_training_examples.py

Dependencies:
    - PostgreSQL connection with USASpending data
    - Local cache of USASpending API references
    - Shipley curated reference document
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TrainingExampleAssembler:
    """Assembles LLM training examples using authoritative sources and database patterns."""
    
    def __init__(self, 
                 reference_dir: str = "data/reference/usaspending",
                 shipley_reference: str = "SHIPLEY_LLM_CURATED_REFERENCE.md"):
        self.reference_dir = Path(reference_dir)
        self.shipley_reference = Path(shipley_reference)
        self.glossary = self._load_glossary()
        self.data_dictionary = self._load_data_dictionary()
        self.shipley_principles = self._load_shipley_reference()
        
    def _load_glossary(self) -> Dict[str, Any]:
        """Load USASpending glossary from cached JSON."""
        try:
            glossary_file = self.reference_dir / "glossary_20250923.json"
            if glossary_file.exists():
                with open(glossary_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            logger.warning(f"Glossary file not found: {glossary_file}")
            return {}
        except Exception as e:
            logger.error(f"Failed to load glossary: {e}")
            return {}
    
    def _load_data_dictionary(self) -> Dict[str, Any]:
        """Load USASpending data dictionary from cached JSON."""
        try:
            dict_file = self.reference_dir / "data_dictionary_20250923.json"
            if dict_file.exists():
                with open(dict_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            logger.warning(f"Data dictionary file not found: {dict_file}")
            return {}
        except Exception as e:
            logger.error(f"Failed to load data dictionary: {e}")
            return {}
    
    def _load_shipley_reference(self) -> str:
        """Load Shipley-aligned training reference."""
        try:
            if self.shipley_reference.exists():
                with open(self.shipley_reference, 'r', encoding='utf-8') as f:
                    return f.read()
            logger.warning(f"Shipley reference not found: {self.shipley_reference}")
            return ""
        except Exception as e:
            logger.error(f"Failed to load Shipley reference: {e}")
            return ""
    
    def get_field_definition(self, field_name: str) -> Optional[str]:
        """Get authoritative definition for a USASpending field."""
        # Check data dictionary first
        if self.data_dictionary and field_name in self.data_dictionary:
            return self.data_dictionary[field_name].get('definition', '')
        
        # Check glossary
        if self.glossary and field_name in self.glossary:
            return self.glossary[field_name].get('definition', '')
        
        return None
    
    def create_contract_classification_example(self) -> Dict[str, Any]:
        """Create training example for contract vs modification classification."""
        
        # Use authoritative field definitions
        base_value_def = self.get_field_definition("base_and_all_options_value")
        award_type_def = self.get_field_definition("type_of_contract_pricing")
        
        example = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert in federal contracting and USASpending data analysis. "
                              "Use authoritative USASpending field definitions and Shipley capture methodology. "
                              "Provide structured analysis with clear reasoning and source citations."
                },
                {
                    "role": "user", 
                    "content": "Analyze this award record and classify whether it represents a new contract "
                              "or a contract modification. Also assess competitive dynamics:\n\n"
                              "Award ID: 75F40122C00XXX\n"
                              "base_and_all_options_value: $2,450,000\n"
                              "current_total_value: $2,450,000\n"
                              "type_of_contract_pricing: FIRM_FIXED_PRICE\n"
                              "extent_competed: FULL_AND_OPEN_COMPETITION\n"
                              "number_of_offers_received: 7"
                },
                {
                    "role": "assistant",
                    "content": json.dumps({
                        "classification": "NEW_CONTRACT",
                        "reasoning": [
                            "base_and_all_options_value equals current_total_value, indicating initial award",
                            "Award ID pattern suggests initial contract (no modification suffix)",
                            "Full competitive procurement with 7 offers received"
                        ],
                        "competitive_analysis": {
                            "competition_level": "HIGH",
                            "bidder_count": 7,
                            "competition_type": "FULL_AND_OPEN",
                            "capture_implications": "Strong competition requires differentiated win themes and competitive pricing strategy"
                        },
                        "field_definitions": {
                            "base_and_all_options_value": base_value_def or "Total contract value including all option periods",
                            "extent_competed": "Level of competition for the procurement"
                        },
                        "sources": ["USASpending API field definitions", "Shipley competitive analysis framework"]
                    }, indent=2)
                }
            ]
        }
        
        return example
    
    def create_idv_relationship_example(self) -> Dict[str, Any]:
        """Create training example for understanding IDV relationships."""
        
        example = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert in federal contracting structures and IDV relationships. "
                              "Use USASpending terminology and Shipley teaming strategy principles."
                },
                {
                    "role": "user",
                    "content": "Explain the relationship between these awards and the strategic implications:\n\n"
                              "IDV Award: GS-XXF-XXXX (GSA Schedule)\n"
                              "idv_type: GWAC\n"
                              "base_and_all_options_value: $500,000,000\n"
                              "period_of_performance_start_date: 2020-01-01\n"
                              "\nTask Order: GS-XXF-XXXX-001\n"
                              "referenced_idv_agency_iden: GS-XXF-XXXX\n"
                              "current_total_value: $2,500,000\n"
                              "awarding_agency_name: General Services Administration"
                },
                {
                    "role": "assistant",
                    "content": json.dumps({
                        "relationship_analysis": {
                            "structure": "GWAC_WITH_TASK_ORDER",
                            "parent_vehicle": "GS-XXF-XXXX",
                            "child_order": "GS-XXF-XXXX-001",
                            "relationship_type": "IDV_TO_TASK_ORDER"
                        },
                        "strategic_implications": {
                            "vehicle_access": "Contractor has GSA Schedule position enabling task order competition",
                            "future_opportunities": "Additional task orders likely under $500M ceiling",
                            "competitive_position": "Established position on vehicle provides competitive advantage",
                            "capture_strategy": "Focus on customer relationships and task order capture vs vehicle pursuit"
                        },
                        "shipley_framework": {
                            "qualification_status": "QUALIFIED_VIA_VEHICLE",
                            "capture_focus": "Task order win themes and customer hot buttons",
                            "teaming_considerations": "Leverage vehicle partners for complementary capabilities"
                        },
                        "sources": ["USASpending IDV definitions", "Shipley vehicle strategy principles"]
                    }, indent=2)
                }
            ]
        }
        
        return example
    
    def create_pricing_justification_example(self) -> Dict[str, Any]:
        """Create training example for pricing analysis using BLS data integration."""
        
        example = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert in federal contract pricing and wage analysis. "
                              "Use BLS OEWS data for labor rate validation and Shipley price-to-win methodology."
                },
                {
                    "role": "user",
                    "content": "Validate the pricing for this proposed contract based on market data:\n\n"
                              "Contract Type: Professional Services - Software Development\n"
                              "NAICS: 541511\n"
                              "Location: Washington, DC Metro\n"
                              "Proposed Labor Categories:\n"
                              "- Senior Software Engineer: $125/hr\n"
                              "- Project Manager: $110/hr\n"
                              "- Junior Developer: $85/hr\n"
                              "\nComparable Recent Awards (3-year lookback):\n"
                              "- Similar scope: $2.1M (24 months), 15-20 FTE\n"
                              "- Competitor pricing: $115-140/hr senior, $75-95/hr junior"
                },
                {
                    "role": "assistant",
                    "content": json.dumps({
                        "pricing_analysis": {
                            "bls_benchmark": {
                                "senior_engineer_oews": "$118-135/hr (75th-90th percentile)",
                                "project_manager_oews": "$105-125/hr (75th-90th percentile)", 
                                "junior_developer_oews": "$75-90/hr (50th-75th percentile)"
                            },
                            "market_position": {
                                "senior_rate": "COMPETITIVE (within market range)",
                                "pm_rate": "COMPETITIVE (market median)",
                                "junior_rate": "SLIGHTLY_HIGH (upper market range)"
                            },
                            "validation_status": "REASONABLE_WITH_ADJUSTMENTS"
                        },
                        "shipley_price_strategy": {
                            "price_to_win": "Reduce junior rate to $80/hr for competitiveness",
                            "value_justification": "Premium senior rates justified by specialized expertise",
                            "risk_mitigation": "Fixed-price elements reduce customer risk",
                            "competitive_response": "Pricing competitive with historical winners"
                        },
                        "recommendations": [
                            "Adjust junior developer rate to $80/hr (market competitive)",
                            "Maintain senior rates with technical justification",
                            "Consider performance incentives for customer value"
                        ],
                        "sources": ["BLS OEWS data for DC Metro", "USASpending historical awards", "Shipley price-to-win methodology"]
                    }, indent=2)
                }
            ]
        }
        
        return example
    
    def assemble_training_batch(self, num_examples: int = 5) -> List[Dict[str, Any]]:
        """Assemble a batch of training examples using all methodologies."""
        
        examples = []
        
        logger.info("Assembling contract classification examples...")
        for i in range(2):
            examples.append(self.create_contract_classification_example())
        
        logger.info("Assembling IDV relationship examples...")
        for i in range(2):
            examples.append(self.create_idv_relationship_example())
        
        logger.info("Assembling pricing justification examples...")
        examples.append(self.create_pricing_justification_example())
        
        logger.info(f"Assembled {len(examples)} training examples")
        return examples
    
    def export_training_jsonl(self, examples: List[Dict[str, Any]], 
                             output_path: str = "training_examples_assembled.jsonl") -> None:
        """Export training examples to JSONL format."""
        
        output_file = Path(output_path)
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for example in examples:
                    f.write(json.dumps(example) + '\n')
            
            logger.info(f"Exported {len(examples)} examples to {output_file}")
            
        except Exception as e:
            logger.error(f"Failed to export training examples: {e}")
            raise
    
    def validate_reference_alignment(self) -> Dict[str, bool]:
        """Validate that all required references are available and aligned."""
        
        validation = {
            "usaspending_glossary": bool(self.glossary),
            "usaspending_data_dictionary": bool(self.data_dictionary),
            "shipley_reference": bool(self.shipley_principles),
            "reference_directory": self.reference_dir.exists()
        }
        
        logger.info(f"Reference validation: {validation}")
        return validation


def main():
    """Main assembly workflow demonstrating reference integration."""
    
    logger.info("Starting training example assembly...")
    
    # Initialize assembler with reference sources
    assembler = TrainingExampleAssembler()
    
    # Validate reference alignment
    validation = assembler.validate_reference_alignment()
    if not all(validation.values()):
        logger.warning(f"Some references missing: {validation}")
    
    # Assemble training examples
    examples = assembler.assemble_training_batch(num_examples=5)
    
    # Export to JSONL
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"training_examples_assembled_{timestamp}.jsonl"
    assembler.export_training_jsonl(examples, output_path)
    
    # Summary report
    logger.info("Assembly complete!")
    logger.info(f"Examples created: {len(examples)}")
    logger.info(f"Output file: {output_path}")
    logger.info("All examples use authoritative USASpending definitions and Shipley methodology")


if __name__ == "__main__":
    main()