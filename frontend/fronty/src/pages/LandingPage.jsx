import { Link } from "react-router-dom";

const features = [
  { title: "Smart discovery", text: "See people who align with your values, lifestyle, and goals." },
  { title: "Verified profiles", text: "Built with trust in mind so every conversation feels safer." },
  { title: "Meaningful messaging", text: "Match quality matters more than endless swiping." },
];

const metrics = [
  { value: "12k+", label: "verified members" },
  { value: "93%", label: "match satisfaction" },
  { value: "4.9/5", label: "user rating" },
];

export default function LandingPage() {
  return (
    <div className="landing-page">
      <header className="landing-header">
        <div className="brand-inline">
          <div className="brand-mark">K</div>
          <span>Kindred</span>
        </div>

        <nav className="landing-nav">
          <Link to="/login">Login</Link>
          <Link to="/register" className="button button--primary">Create account</Link>
        </nav>
      </header>

      <main className="landing-hero">
        <div className="landing-copy">
          <p className="eyebrow">A better way to meet</p>
          <h1>Meet people who genuinely fit your life.</h1>
          <p className="lead">
            Kindred helps you discover thoughtful matches, spark real conversations, and build deeper connections through a calmer, more intentional dating experience.
          </p>

          <div className="cta-row">
            <Link to="/register" className="button button--primary button--large">Get started</Link>
            <Link to="/login" className="button button--secondary button--large">Log in</Link>
          </div>

          <div className="metric-row">
            {metrics.map((metric) => (
              <div key={metric.label} className="metric-card">
                <strong>{metric.value}</strong>
                <span>{metric.label}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="hero-visual" aria-label="Dating app preview">
          <div className="profile-card">
            <div className="profile-photo profile-photo--hero" />
            <div className="profile-card__body">
              <div className="pill-row">
                <span className="pill">New York</span>
                <span className="pill">26</span>
              </div>
              <h3>Ariana, 26</h3>
              <p>Product designer • Loves slow mornings and good coffee.</p>
            </div>
          </div>

          <div className="mini-floating-card mini-floating-card--top">
            <span>93% match</span>
          </div>

          <div className="mini-floating-card mini-floating-card--bottom">
            <span>👋 5 new likes</span>
          </div>
        </div>
      </main>

      <section className="feature-section">
        {features.map((feature) => (
          <article key={feature.title} className="feature-card">
            <div className="feature-icon">✦</div>
            <h3>{feature.title}</h3>
            <p>{feature.text}</p>
          </article>
        ))}
      </section>
    </div>
  );
}
