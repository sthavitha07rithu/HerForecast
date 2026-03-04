import { Link } from "react-router-dom";

export default function Navigation() {
  const navStyle = {
    display: "flex",
    justifyContent: "center",
    gap: "24px",
    padding: "16px",
    background: "rgba(255,255,255,0.4)",
    backdropFilter: "blur(10px)",
    position: "sticky",
    top: 0,
    zIndex: 1000
  };

  const linkStyle = {
    textDecoration: "none",
    fontWeight: 500,
    color: "#5c5470"
  };

  return (
    <nav style={navStyle}>
      <Link style={linkStyle} to="/">Home</Link>
      <Link style={linkStyle} to="/trends">Trends</Link>
      <Link style={linkStyle} to="/reflection">Reflection</Link>
      <Link style={linkStyle} to="/simulate">Simulate</Link>
      <Link style={linkStyle} to="/chat">Chat</Link>
      <Link style={linkStyle} to="/settings">Settings</Link>
    </nav>
  );
}
