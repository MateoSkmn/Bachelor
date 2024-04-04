import { Component, OnDestroy, OnInit } from '@angular/core';
import { HeaderComponent } from '../../global/components/header/header.component';
import { StyledButtonComponent } from '../../global/components/styled-button/styled-button.component';
import { FormsModule } from '@angular/forms';
import { Subject, Subscription, debounceTime } from 'rxjs';
import { ApiService } from '../../global/service/api.service';
import { RecordListItem } from '../../global/interfaces/record-list-item.interface';
import { ErrorService } from '../../global/service/error.service';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { StarEvaluationComponent } from '../../global/components/star-evaluation/star-evaluation.component';

@Component({
  selector: 'app-lime',
  standalone: true,
  imports: [HeaderComponent, StyledButtonComponent, FormsModule, StarEvaluationComponent],
  templateUrl: './lime.component.html',
  styleUrl: './lime.component.scss'
})
export class LimeComponent implements OnInit, OnDestroy{

  recordIndex: number = 0;
  maxIndex: number = Number.MAX_SAFE_INTEGER;
  recordName: string = '';
  recordList: RecordListItem[] = [];

  formattedText: SafeHtml = '';

  constructor(
    private apiService: ApiService,
    private errorService: ErrorService,
    private sanitizer: DomSanitizer) {}
  
  private recordListSubscription!: Subscription;
  private limeExplanationSubscription!: Subscription;
  private numberValueChangeSubject = new Subject<number>();

  ngOnInit(): void {
    this.recordListSubscription = this.apiService.getRecords().subscribe({
      next: (response) => {
        this.recordList = response.filter(item => item.hasModel);
        this.recordName = this.recordList[0].file_name;
        this.requestLimeExplanation();
      },
      error: (error) => {
        this.errorService.triggerError(error);
      }
    });

    this.numberValueChangeSubject.pipe(
      debounceTime(1000) // Debounce for 1 seconds
    ).subscribe(() => {
      if(this.recordIndex == null) {
        this.recordIndex = 0;
      } else if (this.recordIndex < 0) {
        this.recordIndex *= -1;
      } else if (this.recordIndex > this.maxIndex) {
        this.recordIndex = this.maxIndex;
      }
      this.requestLimeExplanation();
    });
  }

  ngOnDestroy(): void {
    if (this.recordListSubscription) {
      this.recordListSubscription.unsubscribe();
    }
    if (this.limeExplanationSubscription) {
      this.limeExplanationSubscription.unsubscribe();
    }
  }

  setTextAlign(): void {
    const textContainer = document.getElementById("textContainer");
    if (!textContainer) {
      return;
    }

    // Delay the measurement to ensure the layout has been updated
    setTimeout(() => {
      const containerHeight = textContainer.offsetHeight;
      const lineHeight = parseInt(window.getComputedStyle(textContainer).lineHeight);
      const isMultiLine = containerHeight > lineHeight;
      if (isMultiLine) {
        textContainer.style.textAlign = "justify";
      } else {
        textContainer.style.textAlign = "center";
      }
    }, 1);
  }

  requestLimeExplanation() {
    // TODO: Loading Screen
    console.log("Loading...");
    this.limeExplanationSubscription = this.apiService.getLime(this.recordName, this.recordIndex).subscribe({
      next: (response) => {
        this.formattedText = this.colorWordsBasedOnValues(response.text, response.lime_values);
        console.log("Completed");
        this.setTextAlign();
        this.maxIndex = response.max_index
      },
      error: (error) => {
        this.formattedText = "";
        this.errorService.triggerError(error);
      }
    });
  }

  onIndexChange() {
    this.numberValueChangeSubject.next(this.recordIndex);
  }

  onSelectChange(value: string) {
    this.recordName = value;
    this.requestLimeExplanation();
  }

  randomIndex() {
    this.recordIndex = Math.floor(Math.random() * (this.maxIndex + 1));
    this.requestLimeExplanation();
  }

  colorWordsBasedOnValues(text: string, limeValues: any[]): SafeHtml {
    const colorMap: any = {
      1: 'rgba(255, 0, 0, ALPHA)', // red
      2: 'rgba(255, 165, 0, ALPHA)', // orange
      3: 'rgba(255, 255, 0, ALPHA)', // yellow
      4: 'rgba(0, 255, 0, ALPHA)', // lime
      5: 'rgba(0, 200, 0, ALPHA)' // green
    };

    let coloredText = '';

    const words = text.split(/\b/); // Split by word boundaries
    words.forEach((word) => {
      const found = limeValues.find((value) => value.word.toLowerCase() === word.toLowerCase());
      if (found) {
        let alpha = found.value; // Use value as alpha
        if (alpha < 0.001) {
          alpha = 0; // Ensure minimum alpha value
        }
        const color = colorMap[found.index].replace('ALPHA', alpha.toString());
        coloredText += `<span style="background-color: ${color}">${word}</span>`;
      } else {
        coloredText += word;
      }
    });

    // Sanitize the HTML content before returning
    return this.sanitizer.bypassSecurityTrustHtml(coloredText);
  }

  saveEvaluation() {
    console.log('TODO: SAVE')
  }

  openLegende() {
    console.log('Open Legende');
  }
}
