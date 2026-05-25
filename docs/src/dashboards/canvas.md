# Blank Canvas

There's a peculiar moment of paralysis that strikes when you create a dashboard — that infinite white space staring back at you, cursor blinking expectantly, waiting for your first move. It's a feeling any artist knows intimately: the blank canvas syndrome.

Like a painter standing before a pristine white surface, brush in hand, you're suddenly overwhelmed by possibility. Should you start with a bold statement piece—a large visualization that commands attention? Or build up gradually with smaller insights? The options multiply exponentially: bar charts, line graphs, heat maps, scatter plots. Grid layouts or freeform designs. Which metrics deserve the spotlight?

This abundance of choice can be paralyzing. Every decision feels weighted with consequence, and the fear of making the "wrong" choice first can stop you from making any choice at all.

But here's what experienced dashboard designers and accomplished artists both understand: **the tools don't matter nearly as much as the vision**.

A painter doesn't obsess over whether to use oils or acrylics before understanding what they want to express. The medium serves the message, not the other way around. Similarly, the most sophisticated charting library or the trendiest visualization technique means nothing if you haven't first grasped what story your data is trying to tell.

The real work happens before you ever touch the canvas. It's in understanding your data deeply—its fields, its patterns, its context. It's in knowing your audience and what questions keep them up at night. It's in crystallizing the one insight that matters most and building everything else in service of that clarity.
The final measure of success isn't visual dazzle—it's usability. Does your dashboard answer questions or create new ones? Can someone glance at it and understand immediately, or do they need a manual? A beautiful painting that communicates nothing is merely decorative. A dashboard that doesn't drive decisions is just noise with pretty colors.

Ultimately, the data speaks for itself. It guides you, shows you the way. The insights begin to emerge organically, revealing themselves like constellations in the night sky. You are merely a messenger, a storyteller—a conduit through which the data takes form and consciousness. It expresses itself through you, becoming an entity that transcends its own graphical representation, something greater than the sum of its numbers and charts. Your role is simply to let it breathe, to give it voice, to allow its truth to manifest.

The rest is just details.

<div class="carousel-wrapper">
  <div class="main-image-container">
    <img id="mainImage" src="../../assets/dashboards/making_of/draft1.jpeg" alt="Main draft">
  </div>

  <div class="filmstrip">
    <button class="nav-btn" onclick="navigate(-1)">❮</button>
    <div class="thumb-track" id="thumbTrack">
      <img src="../../assets/dashboards/making_of/draft1.jpeg" class="thumb active" onclick="showImage(0)">
      <img src="../../assets/dashboards/making_of/draft2.jpeg" class="thumb" onclick="showImage(1)">
      <img src="../../assets/dashboards/making_of/draft3.jpeg" class="thumb" onclick="showImage(2)">
      <img src="../../assets/dashboards/making_of/draft4.jpeg" class="thumb" onclick="showImage(3)">
      <img src="../../assets/dashboards/making_of/draft5.jpeg" class="thumb" onclick="showImage(4)">
      <img src="../../assets/dashboards/making_of/draft6.jpeg" class="thumb" onclick="showImage(5)">
      <img src="../../assets/dashboards/making_of/draft7.jpeg" class="thumb" onclick="showImage(6)">
      <img src="../../assets/dashboards/making_of/draft8.jpeg" class="thumb" onclick="showImage(7)">
    </div>
    <button class="nav-btn" onclick="navigate(1)">❯</button>
  </div>
</div>

<style>
.carousel-wrapper {
  max-width: 900px;
  margin: 2rem auto;
}

.main-image-container {
  width: 100%;
  margin-bottom: 1rem;
}

#mainImage {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 8px;
}

.filmstrip {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-btn {
  flex-shrink: 0;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border: none;
  padding: 12px 16px;
  font-size: 20px;
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.3s;
}

.nav-btn:hover {
  background: rgba(0, 0, 0, 0.9);
}

.thumb-track {
  flex: 1;
  overflow: hidden;
  display: flex;
  gap: 10px;
  scroll-behavior: smooth;
}

.thumb {
  flex-shrink: 0;
  width: 100px;
  height: 70px;
  object-fit: cover;
  cursor: pointer;
  border-radius: 4px;
  opacity: 0.6;
  transition: opacity 0.3s, transform 0.2s, border-color 0.2s;
  border: 3px solid transparent;
}

.thumb:hover {
  opacity: 0.8;
  transform: scale(1.05);
}

.thumb.active {
  opacity: 1;
  border-color: #3b82f6;
}
</style>

<script>
const images = [
  '../../assets/dashboards/making_of/draft1.jpeg',
  '../../assets/dashboards/making_of/draft2.jpeg',
  '../../assets/dashboards/making_of/draft3.jpeg',
  '../../assets/dashboards/making_of/draft4.jpeg',
  '../../assets/dashboards/making_of/draft5.jpeg',
  '../../assets/dashboards/making_of/draft6.jpeg',
  '../../assets/dashboards/making_of/draft7.jpeg',
  '../../assets/dashboards/making_of/draft8.jpeg'
];

let currentIndex = 0;

function showImage(index) {
  currentIndex = index;
  document.getElementById('mainImage').src = images[index];

  const thumbs = document.querySelectorAll('.thumb');
  thumbs.forEach((thumb, i) => thumb.classList.toggle('active', i === index));

  const track = document.getElementById('thumbTrack');
  const active = thumbs[index];
  if (active) {
    const scrollTarget = active.offsetLeft - (track.offsetWidth / 2) + (active.offsetWidth / 2);
    track.scrollTo({ left: scrollTarget, behavior: 'smooth' });
  }
}

function navigate(direction) {
  showImage((currentIndex + direction + images.length) % images.length);
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowLeft') navigate(-1);
  if (e.key === 'ArrowRight') navigate(1);
});
</script>
