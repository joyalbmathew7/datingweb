import { useEffect, useState } from "react";
import { mediaUrl } from "../api";

export default function PhotoViewer({ photos, initialIndex, onClose }) {
  const [index, setIndex] = useState(initialIndex || 0);

  const current = photos[index];
  const total = photos.length;

  // Prevent background scroll when modal is open
  useEffect(() => {
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "auto";
    };
  }, []);

  // Keyboard navigation
  useEffect(() => {
    function handleKeyDown(e) {
      if (e.key === "Escape") {
        onClose();
      } else if (e.key === "ArrowLeft") {
        setIndex((idx) => (idx - 1 + total) % total);
      } else if (e.key === "ArrowRight") {
        setIndex((idx) => (idx + 1) % total);
      }
    }

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [total, onClose]);

  // Close on outside click
  function handleBackdropClick(e) {
    if (e.target === e.currentTarget) {
      onClose();
    }
  }

  // Navigate to previous photo
  function handlePrev(e) {
    e.stopPropagation();
    setIndex((idx) => (idx - 1 + total) % total);
  }

  // Navigate to next photo
  function handleNext(e) {
    e.stopPropagation();
    setIndex((idx) => (idx + 1) % total);
  }

  if (!current) {
    return null;
  }

  return (
    <div className="photo-viewer-backdrop" onClick={handleBackdropClick}>
      <div className="photo-viewer-container">
        {/* Close button */}
        <button
          type="button"
          className="photo-viewer-close"
          onClick={onClose}
          aria-label="Close photo viewer"
        >
          ✕
        </button>

        {/* Image counter */}
        <div className="photo-viewer-counter">
          {index + 1} / {total}
        </div>

        {/* Main image */}
        <div className="photo-viewer-image-wrapper">
          <img
            src={mediaUrl(current.image)}
            alt={`Photo ${index + 1} of ${total}`}
            className="photo-viewer-image"
          />
        </div>

        {/* Navigation buttons */}
        {total > 1 && (
          <>
            <button
              type="button"
              className="photo-viewer-nav photo-viewer-nav-prev"
              onClick={handlePrev}
              aria-label="Previous photo"
            >
              ‹
            </button>
            <button
              type="button"
              className="photo-viewer-nav photo-viewer-nav-next"
              onClick={handleNext}
              aria-label="Next photo"
            >
              ›
            </button>
          </>
        )}

        {/* Keyboard hint */}
        <div className="photo-viewer-hint">
          {total > 1 && <span>← → to navigate</span>}
          <span>ESC to close</span>
        </div>
      </div>
    </div>
  );
}
