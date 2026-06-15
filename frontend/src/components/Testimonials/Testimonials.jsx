import React, { useRef } from 'react'
import './Testimonials.css'
import next from '../../assets/next-icon.png'
import back from '../../assets/back-icon.png'
import user_1 from '../../assets/user-1.jpg'
import user_2 from '../../assets/user-2.jpg'
import user_3 from '../../assets/user-3.png'
import user_4 from '../../assets/user-4.png'

const Testimonials = () => {

    const slider=useRef();
    let tx=0;
    const slideForward = () =>{
        if (tx>-50){
            tx-=25;
        }
        slider.current.style.transform= `translateX(${tx}%)`;

    }

    const slideBackward = () =>{
        if (tx<0){
            tx+=25;
        }
        slider.current.style.transform= `translateX(${tx}%)`;
    }

  return (
    <div className='testimonials'>
        <img src={next} alt="" className='next-btn' onClick={slideForward}/>
        <img src={back} alt="" className='back-btn' onClick={slideBackward}/>
<div className='slider'>
    <ul ref={slider}>
        <li>
        <div className='slide'>
        <div className='user-info'> 
            <img src ={user_1} alt= ""/>
            <div>
                <h3>Aayush Lamsal</h3>
                <span>CEO</span>
            </div>
            </div>
            <p> ChurnIT has transformed the way we approach customer retention. Their predictive analytics have given us invaluable insights into our customers' behavior, allowing us to take proactive measures. We've seen a significant reduction in churn rates since implementing their solutions. Highly recommended!</p>           
            </div>
            </li>

            <li>
        <div className='slide'>
        <div className='user-info'> 
            <img src ={user_2} alt= ""/>
            <div>
                <h3>Ashutosh Jha</h3>
                <span>Club Service Director</span>
            </div>
            </div>
            <p> Implementing ChurnIT's platform was a game-changer for our company. The actionable insights we gained helped us understand the factors driving customer churn and allowed us to address them effectively. The user-friendly interface made it easy for our team to access and interpret data without needing technical expertise</p>
         </div>
            </li>

            <li>
        <div className='slide'>
        <div className='user-info'> 
            <img src ={user_3} alt =""/>
            <div>
                <h3>Adrin Paudel</h3>
                <span>Streamer</span>
            </div>
            </div>
            <p> We chose ChurnIT for their innovative technology and have not been disappointed. Their predictive models are highly accurate, giving us the foresight to act before customers churn. The platform has paid for itself many times over in retained revenue. We couldn't be more satisfied with the results.</p>           
            </div>
            </li>

            <li>
        <div className='slide'>
        <div className='user-info'> 
            <img src ={user_4} alt =""/>
            <div>
                <h3>Adarsh Acharya</h3>
                <span>Scientist</span>
            </div>
            </div>
            <p> ChurnIT's customized solutions have been instrumental in improving our customer retention rates. The support team is always responsive and provides expert guidance, ensuring we get the most out of the platform. Our clients are happier, and our business is thriving thanks to ChurnIT</p>           
            </div>
            </li>

            </ul>
            </div>      
    </div>
  )
}

export default Testimonials
