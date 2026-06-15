import React, { useState, useEffect } from 'react';
import './Programs.css';
import rate from '../../assets/rate.jpg';
import graph from '../../assets/graph.png';
import retention from '../../assets/retention.jpg';
import notification from '../../assets/notification.jpg';

const Programs = () => {
  const [activeCard, setActiveCard] = useState(null);
  const [foldedCard, setFoldedCard] = useState(null);
  const [isFlipping, setIsFlipping] = useState(false);
  const [cardOrder, setCardOrder] = useState([0, 1, 2, 3]);

  const cardData = [
    {
      image: rate,
      title: "Rate Analysis Dashboard",
      alt: "Rate",
      details: "Track and analyze your business metrics with our comprehensive rate monitoring system. Features include real-time updates, historical trends, and predictive analytics.",
      color: "#FFE5E5"
    },
    {
      image: graph,
      title: "Performance Graphs",
      alt: "Graph",
      details: "Visualize your data with interactive graphs. Monitor key performance indicators and make data-driven decisions with our advanced graphing tools.",
      color: "#E5FFE5"
    },
    {
      image: retention,
      title: "Customer Retention Metrics",
      alt: "Retention",
      details: "Keep track of your customer retention rates with detailed cohort analysis. Understand customer behavior and improve engagement strategies.",
      color: "#E5E5FF"
    },
    {
      image: notification,
      title: "Smart Notifications",
      alt: "Notification",
      details: "Stay updated with intelligent alerts. Get real-time notifications about important events and metrics that matter to your business.",
      color: "#FFF5E5"
    }
  ];

  useEffect(() => {
    const handleClickOutside = (event) => {
      const clickArea = document.querySelector('.clickable-area');
      if (clickArea && !clickArea.contains(event.target)) {
        // Move the active card to the end of the stack
        if (activeCard !== null) {
          const newOrder = [...cardOrder];
          newOrder.splice(newOrder.indexOf(activeCard), 1);
          newOrder.push(activeCard);
          setCardOrder(newOrder);
          setActiveCard(null);
          setFoldedCard(null);
        }
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [activeCard, cardOrder]);

  const handleCardClick = (index) => {
    if (isFlipping) return;

    setIsFlipping(true);
    
    if (activeCard === index) {
      setFoldedCard(foldedCard === index ? null : index);
    } else {
      setFoldedCard(null);
      setActiveCard(index);

      // Move the clicked card to the end of the stack
      const newOrder = [...cardOrder];
      newOrder.splice(newOrder.indexOf(index), 1);
      newOrder.push(index);
      setCardOrder(newOrder);
    }

    setTimeout(() => {
      setIsFlipping(false);
    }, 800);
  };

  return (
    <div className="programs-container">
      <div className="clickable-area">
        <div className={`card-stack ${activeCard !== null ? 'blur' : ''}`}>
          {cardOrder.map((index) => (
            <div
              key={index}
              className={`card-wrapper card-${index + 1} ${
                activeCard === index ? 'active' : ''
              }`}
              style={{ zIndex: activeCard === index ? 10 : 4 - index }}
            >
              <div
                className={`card ${foldedCard === index ? 'folded' : ''} ${
                  isFlipping ? 'flipping' : ''
                }`}
                onClick={() => handleCardClick(index)}
                style={{ '--card-color': cardData[index].color }}
              >
                <div className="card-face card-front">
                  <div className="card-content front-content">
                    <img src={cardData[index].image} alt={cardData[index].alt} className="card-image" />
                    <div className="overlay">
                      <h3>{cardData[index].title}</h3>
                      <div className="click-hint">Click to flip</div>
                    </div>
                  </div>
                </div>
                <div className="card-face card-back">
                  <div className="card-content back-content">
                    <h3>{cardData[index].title}</h3>
                    <p>{cardData[index].details}</p>
                    <div className="click-hint">Click to flip back</div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Programs;