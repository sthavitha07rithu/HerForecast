import WeatherHero from '../components/WeatherHero';
import InsightsSection from '../components/InsightsSection';
import ForecastSection from '../components/ForecastSection';
import CycleBanner from '../components/CycleBanner';
import { cyclePhases } from '../data/cycleData';

export default function HomePage({
    cyclePhase,
    onCyclePhaseChange,
    predictionInfo,
    availableUsers,
    selectedUser,
    onUserChange,
}) {
    const data = cyclePhases[cyclePhase];

    return (
        <>
            {predictionInfo && predictionInfo.source === 'api' && (
                <div style={{
                    display: 'flex',
                    justifyContent: 'center',
                    paddingTop: 'var(--space-md)',
                    animation: 'fade-in-up 0.6s ease-out both',
                }}>
                    <div style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '8px',
                        background: 'rgba(255, 255, 255, 0.4)',
                        backdropFilter: 'blur(12px)',
                        borderRadius: 'var(--radius-full)',
                        padding: '6px 16px',
                        fontSize: '0.65rem',
                        fontFamily: 'var(--font-body)',
                        color: 'var(--text-light)',
                        letterSpacing: '0.05em',
                    }}>
                        <span style={{
                            width: '6px',
                            height: '6px',
                            borderRadius: '50%',
                            background: '#7CD4A0',
                            animation: 'breathe 3s ease-in-out infinite',
                        }} />
                        <span>Predicted by AI</span>
                        <span style={{ opacity: 0.5 }}>·</span>
                        <span>{Math.round(predictionInfo.confidence * 100)}% confidence</span>
                    </div>
                </div>
            )}

            {availableUsers?.length > 1 && (
                <div style={{
                    display: 'flex',
                    justifyContent: 'center',
                    padding: 'var(--space-sm) var(--space-lg) 0',
                }}>
                    <select
                        value={selectedUser ?? ''}
                        onChange={(e) => onUserChange(Number(e.target.value))}
                    >
                        {availableUsers.map((id) => (
                            <option key={id} value={id}>
                                User {id}
                            </option>
                        ))}
                    </select>
                </div>
            )}

            <WeatherHero
                state={data.weatherState}
                title={data.heroTitle}
                message={data.heroMessage}
            />

            <CycleBanner
                phaseData={data}
                currentPhase={cyclePhase}
                onPhaseChange={onCyclePhaseChange}
            />

            <InsightsSection
                nervousSystem={data.nervousSystem}
                emotionalLoad={data.emotionalLoad}
                recovery={data.recovery}
            />

            <ForecastSection
                title={data.forecastTitle}
                message={data.forecastMessage}
            />
        </>
    );
}
