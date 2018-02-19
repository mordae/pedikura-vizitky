#!/usr/bin/make -f

vcfs = $(foreach vcf,$(wildcard vcards/*.vcf),build/$(vcf:.vcf=.pdf))

front := templates/v1-front.svg
back := templates/v1-back.svg

all: cards

cards: ${vcfs}

build/vcards/%.pdf: vcards/%.vcf ${front} ${back}
	@mkdir -p "$(dir $@)"
	grep -ive "^X-" $< | qrencode -m 0 -t svg > $@.qr.svg
	tools/cards.py $< ${front} $@.qr.svg $@.card.svg
	inkscape $@.card.svg --export-pdf=$@.front.pdf
	inkscape ${back} --export-pdf=$@.back.pdf
	rm -f $@
	pdfmerge $@.front.pdf $@.back.pdf $@
	rm -rf $@.*

clean:
	rm -rf build

# EOF
