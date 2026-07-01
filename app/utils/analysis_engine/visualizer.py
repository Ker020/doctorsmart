from settings import settings


class RiskVisualizer:
    """Generate visual representations of risk levels"""
    
    @staticmethod
    def generate_risk_bar(risk_score: int, bar_length: int = None) -> str:
        """
        Generate a visual risk bar.
        
        Args:
            risk_score: Risk score from 0-100
            bar_length: Length of the bar (default from settings)
            
        Returns:
            Visual bar representation like: ██████████░░░░░░░░░░ 50%
        """
        if bar_length is None:
            bar_length = settings.RISK_BAR_LENGTH
        
        # Ensure risk_score is within bounds
        risk_score = max(0, min(100, risk_score))
        
        # Calculate filled and empty portions
        filled_length = int((risk_score / 100) * bar_length)
        empty_length = bar_length - filled_length
        
        # Build the bar
        filled_bar = settings.RISK_BAR_FILLED * filled_length
        empty_bar = settings.RISK_BAR_EMPTY * empty_length
        
        return f"{filled_bar}{empty_bar} {risk_score}%"
    
    @staticmethod
    def generate_colored_risk_bar(risk_score: int, bar_length: int = None, 
                                  use_emoji: bool = True) -> str:
        """
        Generate a colored/emoji-enhanced risk bar.
        
        Args:
            risk_score: Risk score from 0-100
            bar_length: Length of the bar
            use_emoji: Whether to use emoji indicators
            
        Returns:
            Enhanced visual representation
        """
        if bar_length is None:
            bar_length = settings.RISK_BAR_LENGTH
        
        # Basic bar
        bar = RiskVisualizer.generate_risk_bar(risk_score, bar_length)
        
        if not use_emoji:
            return bar
        
        # Add emoji based on severity
        if risk_score == 0:
            emoji = "✅"
            label = "Normal"
        elif risk_score <= 25:
            emoji = "🟢"
            label = "Low Risk"
        elif risk_score <= 50:
            emoji = "🟡"
            label = "Moderate Risk"
        elif risk_score <= 75:
            emoji = "🟠"
            label = "High Risk"
        else:
            emoji = "🔴"
            label = "Critical"
        
        return f"{emoji} {label}\n{bar}"
    
    @staticmethod
    def generate_multi_line_display(risk_score: int, severity: str) -> str:
        """
        Generate a multi-line risk display for console output.
        
        Returns:
            Formatted multi-line string
        """
        bar = RiskVisualizer.generate_risk_bar(risk_score)
        
        display = f"""
╔═══════════════════════════════════════════════╗
║           RISK ASSESSMENT SUMMARY             ║
╠═══════════════════════════════════════════════╣
║ Risk Score: {risk_score:>3}%                              ║
║ Risk Level: {bar}    ║
║ Severity:   {severity:<30}     ║
╚═══════════════════════════════════════════════╝
"""
        return display.strip()
    
    @staticmethod
    def generate_arabic_display(risk_score: int, severity_ar: str) -> str:
        """Generate Arabic-friendly risk display"""
        bar = RiskVisualizer.generate_risk_bar(risk_score)
        
        severity_map = {
            "Normal": "طبيعي",
            "Low": "منخفض",
            "Moderate": "متوسط",
            "High": "عالي",
            "Critical": "حرج"
        }
        
        severity_arabic = severity_map.get(severity_ar, severity_ar)
        
        return f"""
═══════════════════════════════════════════
           تقييم درجة الخطورة
═══════════════════════════════════════════
درجة الخطورة: {risk_score}%
{bar}
مستوى الخطورة: {severity_arabic}
═══════════════════════════════════════════
"""
