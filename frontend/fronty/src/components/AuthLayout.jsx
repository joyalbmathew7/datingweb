export default function AuthLayout({ eyebrow, title, description, children, sideTitle, sideText }) {
  return (
    <div className="auth-shell">
      <div className="auth-panel auth-panel--left">
        <div className="brand-block">
          <div className="brand-mark">K</div>
          <div>
            <p className="eyebrow">Kindred</p>
            <h1>Meet people who fit your world.</h1>
          </div>
        </div>

        <div className="auth-feature-box">
          <p className="eyebrow">Designed for real connection</p>
          <h2>{sideTitle || "Modern dating, made human."}</h2>
          <p>{sideText || "Discover people nearby, match with intention, and build a better dating experience from the very first hello."}</p>
        </div>
      </div>

      <div className="auth-panel auth-panel--right">
        <div className="auth-card">
          {eyebrow && <p className="eyebrow auth-eyebrow">{eyebrow}</p>}
          <h2>{title}</h2>
          {description && <p className="auth-description">{description}</p>}
          {children}
        </div>
      </div>
    </div>
  );
}
